from typing import Dict, Any
from app.domain.interfaces import TeamRepository


class AboutService:
    """Service layer for about page business logic"""

    def __init__(self, team_repository: TeamRepository):
        self.team_repository = team_repository

    def get_about_data(self) -> Dict[str, Any]:
        """Get all data needed for about page"""
        team_members = self.team_repository.get_team_members()
        project_stats = self.team_repository.get_project_stats()

        return {
            "team_members": team_members,
            "project_stats": project_stats
        }