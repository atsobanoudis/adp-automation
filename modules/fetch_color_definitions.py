def fetch_color_definitions(service):
    colors = service.colors().get().execute()
    # Colors are divided into event colors and calendar colors; we focus on event colors here.
    event_colors = colors.get('event', {})
    return event_colors
