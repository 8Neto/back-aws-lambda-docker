from app import handler

work = {
    "name": "John Doe",
}


response = handler(work, {})
print(response)
