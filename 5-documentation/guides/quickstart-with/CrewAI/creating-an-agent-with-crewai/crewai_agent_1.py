from uagents import Agent, Context, Model
import os
from crewai import Agent as CrewAIAgent, Task, Crew, Process
from crewai_tools import SerperDevTool

senior_research_analyst_agent = Agent(
    name="senior_research_analyst_agent",
    seed="senior_research_analyst_agent_seed",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)


class CityRequestModel(Model):
    city: str


class ResearchReportModel(Model):
    report: str


os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPER_API_KEY"] = ""


class SeniorResearchAnalyst:
    def __init__(self):
        """
        Initializes the Senior Research Analyst agent with a search tool.
        """
        self.search_tool = SerperDevTool()

        self.researcher = CrewAIAgent(
            role="Senior Research Analyst",
            goal="Uncover cutting-edge developments in AI and provide weather updates.",
            backstory="""You work at a leading tech think tank.
            Your expertise lies in identifying emerging trends and understanding external factors like weather.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool],
        )

    def create_task(self, city: str) -> Task:
        """
        Creates a task for conducting research on AI advancements and retrieving weather updates.

        Parameters:
        - city: str, the city for which the weather update is requested.

        Returns:
        - Task: The created task with the specified description and expected output.
        """
        task_description = (
            f"Conduct a comprehensive analysis of the latest advancements in AI in 2024. "
            f"Also, use the search tool to provide the current weather update for {city}."
        )

        return Task(
            description=task_description,
            expected_output="Full analysis report with weather data",
            agent=self.researcher,
        )

    def run_process(self, city: str):
        """
        Runs the process for the created task and retrieves the result.

        Parameters:
        - city: str, the city for which the task is run.

        Returns:
        - result: The output from the CrewAI process after executing the task.
        """
        task = self.create_task(city)
        crew = Crew(
            agents=[self.researcher],
            tasks=[task],
            verbose=True,
            process=Process.sequential,
        )
        result = crew.kickoff()
        return result


@senior_research_analyst_agent.on_message(model=CityRequestModel, replies=ResearchReportModel)
async def handle_city_request(ctx: Context, sender: str, msg: CityRequestModel):
    """
    Handles incoming messages requesting city information.

    What it does:
    - Logs the received city name.
    - Runs the research process for the specified city and sends the report back to the sender.

    Parameters:
    - ctx: Context, provides the execution context for logging and messaging.
    - sender: str, the address of the sender agent.
    - msg: CityRequestModel, the received message containing the city name.

    Returns:
    - None: Sends the research report to the sender agent.
    """
    ctx.logger.info(f"Received message from {sender} with city: {msg.city}")
    research_analyst = SeniorResearchAnalyst()
    gather_task_result = research_analyst.run_process(msg.city)
    await ctx.send(sender, ResearchReportModel(report=str(gather_task_result)))


if __name__ == "__main__":
    """
    Starts the communication agent and begins listening for messages.

    What it does:
    - Runs the agent, enabling it to send/receive messages and handle events.

    Returns:
    - None: Runs the agent loop indefinitely.
    """
    senior_research_analyst_agent.run()
