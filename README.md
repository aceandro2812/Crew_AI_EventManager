# Autonomous Event Management Crew with CrewAI

This project leverages the CrewAI framework to simulate an autonomous team of agents working collaboratively to plan and execute an event. The team consists of a Venue Coordinator, a Logistics Manager, and a Marketing and Communications Agent, each equipped with specialized tools and powered by a language model (Gemini) to perform their respective tasks.

## Project Overview

The Autonomous Event Management Crew is designed to automate the key aspects of event planning. It demonstrates the power of multi-agent systems in handling complex, real-world scenarios through a coordinated effort. The project showcases:

-   **Agent Specialization:** Each agent has a specific role, goal, and set of tools tailored to their expertise.
-   **Task Coordination:** Agents work together on interconnected tasks, simulating a real team environment.
-   **Custom Tool Integration:** The project includes custom tools for web searching and website scraping, enhancing the agents' capabilities.
-   **Structured Output:** Utilizing Pydantic models, the agents can produce structured output in JSON format, facilitating easy processing and automation.
-   **Asynchronous Execution:** Tasks can be run asynchronously, enabling parallel processing and mimicking real-world team dynamics.
-   **File I/O:** Agents can generate output files in specified formats (JSON, Markdown), creating persistent records of their work.

## Agents

The crew consists of the following agents:

-   **Venue Coordinator:** Responsible for identifying and booking a suitable venue based on the event's requirements.
-   **Logistics Manager:** Manages all logistical aspects, including catering and equipment setup, ensuring a seamless event experience.
-   **Marketing and Communications Agent:** Crafts compelling marketing campaigns and engages with potential attendees to maximize event participation.

## Tools

The agents utilize the following tools:

-   **`web_search` (Custom Search Tool):** Leverages DuckDuckGo Search to find real-time information about companies, industries, and other relevant details.
-   **`scrape_website` (ScrapeWebsiteTool):** Extracts content from websites, allowing agents to gather information from specific web pages.

## Setup

### Prerequisites

Before running the project, ensure you have the following installed:

-   Python 3.10+
-   pip (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    **requirements.txt**
    ```
    crewai
    crewai-tools
    langchain_community
    pydantic
    ```

3.  **Set up API Key:**

    -   Replace `xyz` with your actual Gemini API key in the script.
    -   **Important:** For security reasons, consider using environment variables to store sensitive information like API keys. You can set the API key as an environment variable and then modify the code to read it from there.

    ```python
    import os
    # ... other imports ...

    gemini_api_key = os.environ.get("GEMINI_API_KEY")  # Get API key from environment variable

    gemini_llm = LLM(
        model="openai/gemini-2.0-flash-exp",
        temperature=0.7,
        base_url="[https://generativelanguage.googleapis.com/v1beta/openai/](https://generativelanguage.googleapis.com/v1beta/openai/)",
        api_key=gemini_api_key
    )
    ```

## Usage

1.  **Modify Event Details (Optional):**

    -   You can customize the event details in the `event_details` dictionary within the script. Change the `event_topic`, `event_city`, `tentative_date`, `expected_participants`, and other parameters as needed.

2.  **Run the Script:**

    ```bash
    python main.py
    ```

    Replace `main.py` with the actual name of your Python file.

## Output

The script will generate the following outputs:

-   **`venue_details.json`:** A JSON file containing details about the selected venue, structured according to the `VenueDetails` Pydantic model.
-   **`marketing_report.md`:** A Markdown file summarizing the marketing activities and attendee engagement.
-   **Console Output:** The script will print verbose output to the console, showing the agents' thought processes, actions, and results. After the crew has finished the tasks, the content of `venue_details.json` will be pretty-printed to the console.

## Customization

### Adding Agents

To add more agents to the crew:

1.  **Define the Agent:** Create a new `Agent` instance with a unique role, goal, backstory, and set of tools.
2.  **Create Tasks:** Define tasks specific to the new agent using the `Task` class.
3.  **Add to Crew:** Include the new agent and their tasks in the `Crew` definition.

### Creating Custom Tools

To create custom tools:

1.  **Define Tool Input (Optional):** Create a Pydantic model (like `SearchToolInput`) to define the expected input for your tool.
2.  **Create Tool Class:** Subclass `BaseTool` and implement the `_run` method to define the tool's functionality.
3.  **Assign to Agents:** Add the new tool to the `tools` list of the relevant agents.

### Modifying Tasks

You can modify existing tasks by changing their description, expected output, and other parameters. You can also use embedded inputs (like `{event_city}`) to make the task descriptions more dynamic.

## Future Enhancements

-   **UI Integration:** Develop a user interface (e.g., using Streamlit, Gradio, or Flask) to allow users to interact with the crew more easily.
-   **Error Handling and Robustness:** Implement more robust error handling and retry mechanisms to make the agents more resilient to failures.
-   **Dynamic Task Allocation:** Explore ways to dynamically allocate tasks to agents based on their current workload and capabilities.
-   **Integration with External Services:** Integrate with other services like calendar APIs, email providers, and CRM systems to further automate event management tasks.
-   **Human-in-the-Loop:** Incorporate mechanisms for human review and approval at specific stages of the event planning process.

## Contributing

Contributions to this project are welcome! Please follow these guidelines when contributing:

1.  **Fork the repository.**
2.  **Create a new branch for your feature or bug fix.**
3.  **Make your changes and commit them with clear, descriptive messages.**
4.  **Push your branch to your forked repository.**
5.  **Submit a pull request to the main repository.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. (You'll need to create a LICENSE file in your repository and choose a suitable license like MIT).

## Acknowledgements

-   The CrewAI Framework for providing the foundation for this project.
-   The LangChain community for the tools and integrations used.
-   Google for the Gemini language model.
-   Pydantic for data validation and structured output.
