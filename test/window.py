from app import d

def action(d):
    print(f"window.action() called: {d.value}")
    print(f"d.address = {d}")
    d.add_data()
    return d

action(d)