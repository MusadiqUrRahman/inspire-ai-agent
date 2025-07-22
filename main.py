# from flask import Flask, request, render_template, jsonify
# from agents.extensions.models.litellm_model import LitellmModel
# from agents import Agent, Runner,function_tool, set_tracing_disabled
# from dotenv import load_dotenv
# import asyncio
# import os
# from tavily import TavilyClient
# import webbrowser
# import threading

# # Load environment variables from .env file
# load_dotenv()

# my_model = LitellmModel(api_key=os.getenv("GEMINI_API_KEY"), model="gemini/gemini-2.0-flash-exp",)

# set_tracing_disabled(True)

# # Initialize Flask app
# app = Flask(__name__)


# @function_tool
# def tavily_tool(user_input:str):
#     """search tools"""
#     tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#     response = tavily_client.search(query=user_input)

#     #print(response)
#     return response
#     #return json.dumps(response)


# # Create the InspireAI agent using Gemini model
# def agent_creator():
#     return Agent(
#         name="InspireAI",
#         instructions= """
#                        You are InspireAI – a compassionate, uplifting, and wise AI assistant. 
#                        Your mission is to guide the user with heartfelt words, spiritual reflection, and thoughtful advice. 
#                        Speak like a caring friend, combining motivation, inspiration, and light-hearted humor when appropriate. 
#                        Format your responses beautifully using Markdown – with short paragraphs, bold or italic highlights, lists, and quotes if needed.

#                        Your response should leave the user feeling better, stronger, and more hopeful. 
#                        Every reply should feel human, helpful, and soothing – like a gentle breeze on a stressful day.
#                         """,
        
#         tools=[tavily_tool],
#         model=my_model,

#     )

# # Homepage route
# @app.route("/")
# def index():
#     return render_template("index.html")  # Make sure templates/index.html exists

# # Ask route (POST) - handles user input
# @app.route("/ask", methods=["POST"])
# def ask():
#     user_message = request.json.get("message")
#     agent = agent_creator()

#     history = [{"role": "user", "content": user_message}]

#     try:
#         # Create an async event loop manually
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         # Run the agent using the runner
#         response = loop.run_until_complete(
#             Runner.run(starting_agent=agent, input=history)
#         )

#         loop.close()

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

#     return jsonify({"response": response.final_output})

# # Run the Flask server
# # if __name__ == "__main__":
# #     app.run(debug=True)



# def open_browser():
#     webbrowser.open_new("http://127.0.0.1:5000")

# if __name__ == "__main__":
#     threading.Timer(1.5, open_browser).start()
#     app.run(debug=True)


# ================================================================================

from flask import Flask, request, render_template, jsonify
from agents.extensions.models.litellm_model import LitellmModel
from agents import Agent, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
import asyncio
import os
from tavily import TavilyClient
import webbrowser
import threading

# Load environment variables from .env file
load_dotenv()

# Initialize model
my_model = LitellmModel(
    api_key=os.getenv("GEMINI_API_KEY"),
    model="gemini/gemini-2.0-flash-exp",
)

set_tracing_disabled(True)

app = Flask(__name__)


@function_tool
def tavily_tool(user_input: str):
    """Search tool using Tavily API"""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query=user_input)
    return response


def agent_creator():
    return Agent(
        name="InspireAI",
        instructions="""
            You are InspireAI – a compassionate, uplifting, and wise AI assistant.
            Your mission is to guide the user with heartfelt words, spiritual reflection, and thoughtful advice.
            Speak like a caring friend, combining motivation, inspiration, and light-hearted humor when appropriate.
            Format your responses beautifully using Markdown.
        """,
        tools=[tavily_tool],
        model=my_model,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_message = request.json.get("message")
        agent = agent_creator()
        history = [{"role": "user", "content": user_message}]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(
            Runner.run(starting_agent=agent, input=history)
        )
        loop.close()

        return jsonify({"response": response.final_output})

    except Exception as e:
        print("⚠️ ERROR:", e)
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
