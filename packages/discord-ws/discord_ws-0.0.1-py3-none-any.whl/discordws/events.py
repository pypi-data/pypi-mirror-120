# store event's in module
__events = dict()

def event(func):
    
    # check if key exists
    if func.__name__ not in __events:
        __events[func.__name__] = []
    
    # add event
    __events[func.__name__].append(func)

async def handle_event(ctx, payload):
    
    # create key from payload event name
    key = "on_" + payload["t"].lower()
    
    # check if payload exists in events
    if key not in __events or not isinstance(__events[key], list):
        return # do nothing
    
    for event in __events[key]:
        ctx.loop.create_task(event(payload))