from rest_framework import serializers
from .models import UserProfile, Skill
from apps.accounts.serializers import UserDetailSerializer

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    skills = serializers.SerializerMethodField()
    skills_input = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True,
        required=False,
        help_text="List of skill names e.g. ['React', 'Django', 'Python', 'PostgreSQL']"
    )

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'job_role',
            'years_of_experience',
            'location',
            'education',
            'current_salary',
            'skills',
            'skills_input',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

    def get_skills(self, obj):
        return SkillSerializer(obj.skills.all(), many=True).data

    def validate_years_of_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 60:
            raise serializers.ValidationError("Years of experience cannot exceed 60 years.")
        return value

    def validate_current_salary(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value

    def _sync_skills(self, profile, skill_names):
        """Helper to normalize and associate skills with profile."""
        if skill_names is not None:
            skill_objs = []
            for raw_name in skill_names:
                clean_name = raw_name.strip()
                if clean_name:
                    # Case-insensitive lookup or create
                    existing = Skill.objects.filter(name__iexact=clean_name).first()
                    if existing:
                        skill_objs.append(existing)
                    else:
                        new_skill = Skill.objects.create(name=clean_name)
                        skill_objs.append(new_skill)
            profile.skills.set(skill_objs)

    def create(self, validated_data):
        skills_input = validated_data.pop('skills_input', [])
        user = self.context['request'].user
        
        # Ensure user doesn't already have a profile
        if hasattr(user, 'profile'):
            raise serializers.ValidationError("A profile already exists for this user.")

        profile = UserProfile.objects.create(user=user, **validated_data)
        self._sync_skills(profile, skills_input)
        return profile

    def update(self, instance, validated_data):
        skills_input = validated_data.pop('skills_input', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if skills_input is not None:
            self._sync_skills(instance, skills_input)

        return instance
