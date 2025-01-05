from openai import OpenAI
from dotenv import load_dotenv
from string import Template

load_dotenv()
client = OpenAI()

prompt_template = Template(
    """
Product Name: $product_name
Relevant information about the product:
$product_text
Given the above data of product reviews, metadata and user interactions, your task is to:
Identify and extract relevant questions and their corresponding answers from each interaction.
Ensure the generated QA-pairs are accurate and relevant to the original reviews and metadata.
Ensure that the question is tailored to the a user who has interacted with the following products:
$user_trajectory
Do not number your responses. Instead, separate each response with a newline.
Answer in the following format: "<question>|<answer>" (without the quotes).
"""
)


def get_response(
    product_name: str, product_text: str, user_trajectory: str, print_prompt: str = ""
) -> str:
    prompt = prompt_template.substitute(
        product_name=product_name,
        product_text=product_text,
        user_trajectory=user_trajectory,
    )
    if print_prompt:
        with open(print_prompt, "w") as f:
            f.write(prompt)
    return (
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
            temperature=0.5,
            max_tokens=256,
            top_p=1,
        )
        .choices[0]
        .message.content
    )
