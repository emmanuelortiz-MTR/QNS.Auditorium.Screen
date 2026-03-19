INDEX_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projector Guide</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #007bff; color: white; text-decoration: none; border-radius: 8px; }}
        img, video, iframe {{ max-width: 100%; height: auto; margin: 1rem 0; }}
        iframe {{ width: 100%; height: 340px; border: none; }}
        .nav {{ margin-top: 2rem; }}
        .nav a {{ margin-right: 1rem; }}
    </style>
</head>
<body>
    <h1>So you want to operate the Auditorium Main Projector?</h1>
    {options_html}
</body>
</html>
"""

STEP_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Step {step_num} of {total_steps} – {option_title}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #007bff; color: white; text-decoration: none; border-radius: 8px; }}
        img, video, iframe {{ max-width: 100%; height: auto; margin: 1rem 0; }}
        iframe {{ width: 100%; height: 340px; border: none; }}
        .nav {{ margin-top: 2rem; }}
        .nav a {{ margin-right: 1rem; }}
    </style>
</head>
<body>
    <h1>{option_title}</h1>
    <p><strong>Step {step_num} of {total_steps}</strong></p>
    <p>{instruction}</p>
    {media}
    <div class="nav">
        {prev_link}
        {next_link}
        <a href="index.html">🏠 Home</a>
    </div>
</body>
</html>
"""

CONGRATS_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Congratulations!</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 2rem auto; padding: 0 1rem; text-align: center; }}
        .button {{ display: inline-block; padding: 1rem 2rem; margin: 1rem 0; background: #28a745; color: white; text-decoration: none; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>🎉 Good job! 🎉</h1>
    <p>You have successfully {message}.</p>
    <a href="index.html" class="button">Start another task</a>
</body>
</html>
"""
