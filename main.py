import tkinter as tk
from tkinter import ttk
import openai
import os
from dotenv import load_dotenv


class GPT4Generator:
    def __init__(self, api_key=None):
        # Load API key from .env file if not provided
        if api_key is None:
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")

        openai.api_key = api_key

    def generate_response(self, prompt, model="text-davinci-003", max_tokens=1000):  # Add 'self' parameter
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.8,
        )
        return response.choices[0].text.strip()

class OccupationFeeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x200")
        self.root.title("Occupation Fee Calculator")

        self.occupation_label = tk.Label(self.root, text="Occupation:")
        self.occupation_label.grid(row=0, column=0, padx=5, pady=5)
        self.occupation_entry = tk.Entry(self.root)
        self.occupation_entry.grid(row=0, column=1, padx=5, pady=5)

        self.state_label = tk.Label(self.root, text="State:")
        self.state_label.grid(row=1, column=0, padx=5, pady=5)
        self.state_var = tk.StringVar()
        self.state_dropdown = ttk.Combobox(self.root, textvariable=self.state_var)
        self.state_dropdown['values'] = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
            'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
            'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
            'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
            'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        self.state_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_values)
        self.clear_button.grid(row=2, column=0, padx=5, pady=5)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=2, column=1, padx=5, pady=5)

        self.root.mainloop()

    def clear_values(self):
        self.occupation_entry.delete(0, tk.END)
        self.state_var.set('')

    def submit_values(self):
        occupation = self.occupation_entry.get()
        state = self.state_var.get()
        state_full_name = state.title()  # get the full name of the state
        prompt = "Generate CSV to list the following occupational information for a registered [{occupation}] in the state of {state}: Occupation Name, Agency Website Address, Total Fees for Initial Licensure, Duration of License, Renewal Frequency, Renewal Costs, Renewal Agency, Description of License, Related Keywords, Related NAICS codes, Related ONET codes. Create empty values if one does not exist. Comma separated values in between the brackets indicate multiple occupations which will each need a separate records.".format(
            occupation=occupation, state=state_full_name)  # the prompt to
        generator = GPT4Generator()
        response = generator.generate_response(prompt=prompt)

        response_window = tk.Toplevel(self.root)
        response_window.geometry("300x300")
        response_text = tk.Text(response_window, wrap=tk.WORD, font=("Inconsolata", 16))
        response_text.insert(tk.END, response)
        response_text.pack(expand=True, fill=tk.BOTH)

        tk.Button(response_window, text="Close", command=response_window.destroy).pack(side=tk.BOTTOM)


if __name__ == '__main__':
    OccupationFeeGUI()
