from crewai import Agent, Task, Crew , Process ,LLM
import os
from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import BaseTool
from crewai_tools import ScrapeWebsiteTool
import json
from pprint import pprint


gemini_llm  = LLM(
    model="openai/gemini-2.0-flash-exp",
    temperature=0.7,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key="AIzaSyA6Gd_kJL0g8XCMZXJ-uJwbTDYcac1zqGk"
)


class SearchToolInput(BaseModel):
    query: str = Field(..., description="Search query string")

class SearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search for real-time information about companies and industries"
    args_schema = SearchToolInput
        
    def _run(self, query: str) -> str:
        search = DuckDuckGoSearchRun(region="pt-br")
        return search.run(query)
# tool initialization
search_tool = SearchTool()
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Venue Coordinator
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal="Identify and book an appropriate venue "
    "based on event requirements",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and "
        "understanding of event logistics, "
        "you excel at finding and securing "
        "the perfect venue that fits the event's theme, "
        "size, and budget constraints."
    ),
    llm=gemini_llm
)

 # Agent 2: Logistics Manager
logistics_manager = Agent(
    role='Logistics Manager',
    goal=(
        "Manage all logistics for the event "
        "including catering and equipment"
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Organized and detail-oriented, "
        "you ensure that every logistical aspect of the event "
        "from catering to equipment setup "
        "is flawlessly executed to create a seamless experience."
    ),
    llm=gemini_llm
)


# Agent 3: Marketing and Communications Agent
marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal="Effectively market the event and "
         "communicate with participants",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Creative and communicative, "
        "you craft compelling messages and "
        "engage with potential attendees "
        "to maximize event exposure and participation."
    ),
    llm=gemini_llm
)

# Now here is a pydantic object created so that the output can be structured
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity : int
    booking_status :str

# This pydantic object can be used to structure any output , this would help in getting non fuzzy outputs from the agents which can help in process automation easily

# Tasks
# Please note in the tasks how we have used output_json for the pydantic structure
venue_task = Task(
    description="Find a venue in {event_city} "
                "that meets criteria for {event_topic}.",
    expected_output="All the details of a specifically chosen"
                    "venue you found to accommodate the event.",
    human_input=True,
    output_json=VenueDetails,
    output_file="venue_details.json",  
      # Outputs the venue details as a JSON file
    agent=venue_coordinator
)
# here by setting asyn execution , the tasks become unrelated so parallel tasks run , this can mimic real people working in teams 
logistics_task = Task(
    description="Coordinate catering and "
                 "equipment for an event "
                 "with {expected_participants} participants "
                 "on {tentative_date}.",
    expected_output="Confirmation of all logistics arrangements "
                    "including catering and equipment setup.",
    human_input=True,
    async_execution=True,
    agent=logistics_manager
)

marketing_task = Task(
    description="Promote the {event_topic} "
                "aiming to engage at least"
                "{expected_participants} potential attendees.",
    expected_output="Report on marketing activities "
                    "and attendee engagement formatted as markdown.",
    # async_execution=True,
    output_file="marketing_report.md",  # Outputs the report as a text file
    agent=marketing_communications_agent
)
# Take a note of how '{xyz}' these embedded inputs are used inside the prompts , this helps make the prompt more dynamic

# making the crew
# Define the crew with agents and tasks
event_management_crew = Crew(
    agents=[venue_coordinator, 
            logistics_manager, 
            marketing_communications_agent],
    
    tasks=[venue_task, 
           logistics_task, 
           marketing_task],
    
    verbose=True
)
# here the order of the tasks doesnt matter as they are async , only venue_cordination has to run first

# this is how the inputs for the crew are made (this can be dynamic too , think of a form where these values are entered)
event_details = {
    'event_topic': "Tech Innovation Conference",
    'event_description': "A gathering of tech innovators "
                         "and industry leaders "
                         "to explore future technologies.",
    'event_city': "Mumbai",
    'tentative_date': "2025-01-15",
    'expected_participants': 500,
    'budget': 20000,
    'venue_type': "Conference Hall"
}
# running the crew
result = event_management_crew.kickoff(inputs=event_details)

# printing the data from the json that was generated
with open('venue_details.json') as f:
   data = json.load(f)

pprint(data)
# Lets go this code might get everything done !!
# Future scope:-
"""
we can potentially make a UI based form for this which then can take inputs and show the outputs properly!!
"""