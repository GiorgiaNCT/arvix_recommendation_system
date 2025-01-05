from anthropic import Anthropic

class ClaudeService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    async def generate_paper_insight(self, paper_title: str, paper_link: str) -> str:
        """Generate insights about a research paper using Claude"""
        prompt = f"""
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

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return response.content