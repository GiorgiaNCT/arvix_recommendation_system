from openai import OpenAI



class ChatGPTService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def generate_paper_insight(self, paper_title: str, paper_link: str) -> str:
        """Generate insights about a research paper using ChatGPT"""

        prompt1 = f"""
        As not an AI research expert, 
        but as a Computer Science student in the first year of my Bachelor's degree, 
        analyze this paper at the link {paper_link}
        and provide key insights:

        Please stick to this plan while writing the review:
        1. Title, authors
        2. Problem statement
        3. A short description of the proposed method
        4. Paper's novelty, contribution
        5. Evaluation:
        - datasets for training and evaluation
        - metrics for evaluation
        - conclusions from the comparison with reference to the tables and the figures
        - ablation study ideas and results
        6. Advantages and shortcomings
        7. (optional) Usefulness for production
        8. Find additional information about this paper: project page, GitHub repo, and Hugging Face demo
        
        """
        prompt2 = f"""
        As a Computer Science student in the first year of my Bachelor's degree, 
        analyze this paper at the link {paper_link}
        and provide key insights:
        Please stick to this plan while writing the review:
        1. Problem statement
        2. A short description of the proposed method
        3. Paper's novelty, contribution
        4. Evaluation:
        - datasets for training and evaluation
        - metrics for evaluation
        - conclusions from the comparison with reference to the tables and the figures
        - ablation study ideas and results
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Computer Science student in the first year of my Bachelor's degree."},
                {"role": "user", "content": prompt2}
            ],
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].message.content