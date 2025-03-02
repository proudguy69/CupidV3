import asyncio


from Cupidv3Backend.server import app


async def main():
    app.run(debug=True)
    
    

if __name__ == "__main__":
    asyncio.run(main())
    