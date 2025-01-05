import os
import httpx
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from app.services.arxiv import ArxivService
from app.models.schemas import SearchResponse
from app.services.chatgpt import ChatGPTService
from app.services.claude import ClaudeService

#OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
#chatgpt = ChatGPTService(api_key=OPENAI_API_KEY)

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
claude = ClaudeService(api_key=ANTHROPIC_API_KEY)

# Command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /start command"""
    await update.message.reply_text('Hello! I am your bot!')

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /hello command"""
    await update.message.reply_text('Hello! this is hello function!')


async def get_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /get command"""
    try:
        # Make API call to your FastAPI endpoint
        query = "cat:cs.AI"
        max_results = 1
        papers = ArxivService.fetch_papers(
            search_query=query,
            max_results=max_results,
            start=0,
            sort_by='lastUpdatedDate',
            sort_order='descending'
        )
        
        if papers and len(papers) > 0:
            paper = papers[0]  # Get the first paper
            paper_preprocessed_link = paper['link'].replace('abs', 'pdf')
            """
            # Get ChatGPT analysis
            analysis = await chatgpt.generate_paper_insight(
                paper['title'],
                paper_preprocessed_link
            )
            """

            # Get Claude analysis instead of ChatGPT
            analysis = await claude.generate_paper_insight(
                paper['title'],
                paper_preprocessed_link
            )

            message = (
                f"📚 *AI Paper Recommendation*\n\n"
                f"*Title:* {paper['title']}\n"
                f"*Authors:* {', '.join(author['name'] for author in paper['authors'])}\n"
                f"*Published:* {paper['published']}\n"
                f"*Link:* {paper['link']}"
                f"🤖 *Claude Analysis:*\n{analysis}"
            )

            
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("No papers found.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


BOT_TOKEN = os.environ.get('BOT_TOKEN')
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    hello_handler = CommandHandler('hello', hello)
    get_handler = CommandHandler('get', get_command)

    application.add_handler(start_handler)
    application.add_handler(hello_handler)
    application.add_handler(get_handler)
    
    application.run_polling()

if __name__ == "__main__":
   main()