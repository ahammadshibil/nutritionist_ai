import gradio as gr
import openai
import os
import re

# Fetching the API key from the environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable before running the script.")

def ask_gpt3(prompt):
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7,
    )
    message = response.choices[0].text.strip()
    message = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', message)
    return message

def generate_diet_plan(food_prefs, restrictions, budget, height, weight, goals, preferences):
    prompt = f"Based on your food preferences ({food_prefs}), dietary restrictions ({restrictions}), weekly budget ({budget}), height ({height} cm), weight ({weight} kg), fitness goals ({goals}), and additional preferences in your diet program ({preferences}), here is your personalized diet plan:"
    diet_plan = ask_gpt3(prompt)
    return diet_plan

iface = gr.Interface(
    fn=generate_diet_plan,
    inputs=["text", "text", "text", "text", "text", "text", "text"],
    outputs="text",
    title="Nutritionist AI",
    description="Generate a personalized diet plan based on your inputs.",
    examples=[
        ["Vegetarian", "None", "$50", "170", "65", "Lose weight", "High protein"],
        ["Non-vegetarian", "Lactose intolerance", "$70", "165", "70", "Maintain weight", "Keto"],
    ],
)

if __name__ == "__main__":
    iface.launch()
