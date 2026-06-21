import os
import json
from typing import Dict, Any, List

class AgentContext:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.memory_bank: List[Dict[str, Any]] = []

    def update_state(self, key: str, value: Any):
        self.memory_bank.append({"key": key, "value": value})

class CustomMCPServer:
    """Mock Model Context Protocol (MCP) server providing local sustainability data metrics."""
    @staticmethod
    def fetch_climate_metrics(region: str) -> Dict[str, Any]:
        # Local environmental data engine mapping - Normalized case-insensitive lookup
        database = {
            "surat": {"carbon_index": 78.5, "ev_adoption_rate": "12%", "solar_capacity_mw": 450, "air_quality": "Moderate"},
            "mumbai": {"carbon_index": 92.1, "ev_adoption_rate": "18%", "solar_capacity_mw": 120, "air_quality": "Poor"},
            "delhi": {"carbon_index": 98.4, "ev_adoption_rate": "10%", "solar_capacity_mw": 85, "air_quality": "Severe"},
            "bangalore": {"carbon_index": 62.3, "ev_adoption_rate": "22%", "solar_capacity_mw": 310, "air_quality": "Good"}
        }
        # Dynamic fallback for unlisted regions
        return database.get(region.lower(), {"carbon_index": 55.0, "ev_adoption_rate": "7%", "solar_capacity_mw": 40, "air_quality": "Good"})

class SustainabilityAgentSystem:
    def __init__(self, session_id: str):
        self.ctx = AgentContext(session_id)
        self.mcp = CustomMCPServer()

    def data_analyzer_agent(self, region: str) -> Dict[str, Any]:
        """Sub-agent 1: Fetches and checks structural climate parameters via MCP."""
        metrics = self.mcp.fetch_climate_metrics(region)
        
        # Dynamic threshold evaluation logic
        if metrics["carbon_index"] > 85:
            metrics["urgency_status"] = "CRITICAL"
            metrics["primary_recommendation"] = "Impose immediate heavy emission caps & mandate green transport zones."
        elif metrics["carbon_index"] > 70:
            metrics["urgency_status"] = "HIGH"
            metrics["primary_recommendation"] = "Accelerate urban solar canopy deployments & incentivize EV infrastructure."
        else:
            metrics["urgency_status"] = "STABLE"
            metrics["primary_recommendation"] = "Optimize existing green infrastructure networks and maintain monitors."
        
        self.ctx.update_state(f"{region}_metrics", metrics)
        return metrics

    def report_generator_agent(self, region: str, analytics: Dict[str, Any]) -> str:
        """Sub-agent 2: Transforms structured data into actionable insights."""
        report = (
            f"\n=== SUSTAINABILITY ACTION REPORT FOR {region.upper()} ===\n"
            f"Current Air Quality: {analytics['air_quality']}\n"
            f"Carbon Footprint Index: {analytics['carbon_index']} units\n"
            f"Current EV Adoption: {analytics['ev_adoption_rate']}\n"
            f"Strategic Urgency Level: {analytics['urgency_status']}\n\n"
            f"PROPOSED AGENT ACTION PLAN:\n"
            f"1. Action Item: {analytics['primary_recommendation']}\n"
            f"2. Infrastructure Milestone: Expand target past {analytics['solar_capacity_mw']} MW within 18 months.\n"
            f"======================================================="
        )
        self.ctx.update_state(f"{region}_final_report", report)
        return report

    def run_coordinator_workflow(self, target_region: str) -> str:
        """Main Coordinator Orchestrator managing sequential agent data flow."""
        analysis_payload = self.data_analyzer_agent(target_region)
        final_output = self.report_generator_agent(target_region, analysis_payload)
        return final_output

if __name__ == "__main__":
    orchestrator = SustainabilityAgentSystem(session_id="sess_001_climate_demo")
    
    print("Welcome to EcoAgent Multi-Agent Workspace!")
    print("Available database profiles: Surat, Mumbai, Delhi, Bangalore (or type any other city for a standard evaluation)")
    
    # Allows the user to interact dynamically during your demo video
    user_city = input("\nEnter the city name to evaluate: ").strip()
    
    if user_city:
        result_report = orchestrator.run_coordinator_workflow(target_region=user_city)
        print(result_report)
    else:
        print("Invalid input. Exiting workflow.")
