import pdfkit
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
  loader = FileSystemLoader("."),
  autoescape = select_autoescape,
)

template = env.get_template("template.html")


def dict_to_pdf(data_dict):
    """
    Process the data dictionary.

    Args:
        data_dict (dict): A dictionary containing the following keys:
                          - 'name' (str): The name of the person.
                          - 'title' (str): Title of the task done.
                          - 'task_desc' (str): description of task. Preferably just one line
                          - 'task_summary' (list of str): each entry in the list will be a new bullet point
                          - 'faith_score' (int): faith score calculated if you wanna change the thresholds edit in this py file.

    Returns:
        pdf_data: The final pdf 
    """
    
    
    loc = "Garching"
    desc = ""
    code_eq = ""
    desc_equip = ""
    no = ""
    subj = ""
    ord_cust = ""
    no_op = ""
    no_not = ""
    no_type = ""
    period = ""
    name = data_dict['name']
    task_description = data_dict["task_desc"]
    reason_and_solution = data_dict["task_summary"]
    service_title = data_dict["title"]
    faith_score = data_dict["faith"]

    if faith_score < 3:
        faith = "G"
    elif faith_score < 6: 
        faith = "Y"
    else:
        faith = "R"

    html = template.render(
            service_title = service_title,
            name = name,
            faith = faith,
            loc = loc,
            desc = desc,
            code_eq = code_eq,
            desc_equip = desc_equip,
            no = no,
            subj = subj,
            ord_cust = ord_cust,
            no_op = no_op,
            no_not = no_not,
            no_type = no_type,
            period = period,
            date = date.today(),
            task_description = task_description,
            reason_description = reason_and_solution
        )

    return pdfkit.from_string(html, None) 
