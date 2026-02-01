from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import VerifiedEmailPermission
from .serializers import OrganizationSerializer
from .models import OrganizationMember
from accounts.models import User
from django.db import transaction
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError

# Create Organization
class CreateOrganization_View(APIView):
    permission_classes = [VerifiedEmailPermission]
    def post(self, request):
        data = request.data
        organization_serializer = OrganizationSerializer(data=data)
        if organization_serializer.is_valid():
            organization_serializer.save()
            return Response({"message": "Organization created successfully"}, status=201)
        return Response(organization_serializer.errors, status=400)


# Change onership of organization
class ChangeOwnerOrganizationView(APIView):
    permission_classes = [VerifiedEmailPermission]

    @transaction.atomic
    def post(self, request, org_id):
        user = request.user
        new_owner_email = request.data.get("new_owner_email")

        if not new_owner_email:
            raise ValidationError("new_owner_email is required")

        # 1️⃣ Verify current user is OWNER of this org
        try:
            current_owner_membership = OrganizationMember.objects.get(
                organization_id=org_id,
                user=user,
                role=OrganizationMember.Role.OWNER
            )
        except OrganizationMember.DoesNotExist:
            raise PermissionDenied("Only the owner can transfer ownership")

        # 2️⃣ Prevent self-transfer
        if user.email == new_owner_email:
            raise ValidationError("New owner must be different from current owner")

        # 3️⃣ Get new owner user
        new_owner_user = get_object_or_404(User, email=new_owner_email)

        if not new_owner_user.is_email_verified:
            raise ValidationError("New owner must have a verified email")

        # 4️⃣ Ensure new owner is already a member of the org
        try:
            new_owner_membership = OrganizationMember.objects.get(
                organization_id=org_id,
                user=new_owner_user
            )
        except OrganizationMember.DoesNotExist:
            raise ValidationError("User must already be a member of the organization")

        # 5️⃣ Swap roles (atomic)
        current_owner_membership.role = OrganizationMember.Role.MEMBER
        current_owner_membership.save(update_fields=["role"])

        new_owner_membership.role = OrganizationMember.Role.OWNER
        new_owner_membership.save(update_fields=["role"])

        return Response(
            {"msg": "Organization ownership transferred successfully"},
            status=status.HTTP_200_OK
        )
