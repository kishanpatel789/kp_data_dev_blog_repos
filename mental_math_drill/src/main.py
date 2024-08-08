import json
import boto3
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from problem import generate_problems, Problem
from greeting import generate_greeting
from jinja2 import Environment, FileSystemLoader
from typing import Any, Dict

def main(*args: Any) -> Dict[str, Any]:
    """
    Main function to generate math problems, render them into text and HTML templates, 
    and send them via email using AWS SES.

    Args:
        *args (Any): Variable length argument list.

    Returns:
        Dict[str, Any]: A dictionary containing the status code and message ID of the sent email.
    """
    # read environment vars
    sender = os.environ['MMD_SENDER']
    recipient = os.environ['MMD_RECIPIENT']
    num_probs = int(os.environ.get('MMD_NUM_PROBS', '5'))
    bool_operators = [
        bool(int(os.environ.get('MMD_USE_ADD', '1'))),
        bool(int(os.environ.get('MMD_USE_SUB', '1'))),
        bool(int(os.environ.get('MMD_USE_MUL', '0'))),
        bool(int(os.environ.get('MMD_USE_DIV', '0'))),
    ]

    # select operators based on environment variables
    selected_ops = [o for o, use_op in zip(Problem.valid_operators, bool_operators) if use_op]

    # generate problems and html
    greeting = generate_greeting()
    problems = generate_problems(num_probs, selected_ops)
    env = Environment(
        loader=FileSystemLoader('./templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template_txt = env.get_template('template.txt')
    template_html = env.get_template('template.html')

    output_txt = template_txt.render(problems=problems, greeting=greeting)
    output_html = template_html.render(problems=problems, greeting=greeting)
    # with open('../out/out.txt', 'w') as f:
    #     f.write(output_txt)
    # with open('../out/out.html', 'w') as f:
    #     f.write(output_html)

    # generate email
    subject = f"Mental Math Drill - {datetime.today().strftime('%m/%d')}"

    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    message.attach(MIMEText(output_txt, 'plain'))
    message.attach(MIMEText(output_html, 'html'))

    # send email
    ses = boto3.client('sesv2')
    response = ses.send_email(
        Content={
            'Raw': {
                'Data': message.as_bytes()
            }
        }
    )

    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(f"Email sent successfully. MessageId is: {response['MessageId']}")
    }

if __name__ == '__main__':
    response = main()
    print(response)