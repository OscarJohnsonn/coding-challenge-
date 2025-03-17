import tkinter as tk
from tkinter import filedialog, scrolledtext  
from log_processor import LogProcessor  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  


def analyze_log():
    #open file dialog to select a log file
    file_path = filedialog.askopenfilename(
        filetypes=[("Log files", "*.log"), ("All files", "*.*")]
    )
    if file_path:
        #create a LogProcessor instance and parse the log file
        processor = LogProcessor(file_path)
        processor.parse_log()

        #clear previous results
        result_text.delete(1.0, tk.END)

        
        result_text.insert(
            tk.END,
            f"Total jobs: {len(processor.jobs)}\nIncomplete:"
            f" {len(processor.incomplete_jobs)}\nOverlapping:"
            f" {len(processor.overlapping_jobs)}\n\n",
        )

        #display details for each job
        for pid, job in processor.jobs.items():
            #if job is incomplete or overlapping
            job_status = ""
            is_incomplete = pid in processor.incomplete_jobs
            is_overlapping = pid in processor.overlapping_jobs

            if is_incomplete:
                job_status = " [INCOMPLETE]"
            if is_overlapping:
                job_status += " [OVERLAPPING]"

            #add job information to the text 
            result_text.insert(
                tk.END,
                f"Job {pid}: {job.description} - Duration: {job.get_duration()}s"
                f"{job_status} "
                f"{'(ERROR)' if job.is_error() else '(WARNING)' if job.is_warning() else ''}\n",
            )

            #apply highlighting for incomplete overlapping jobs
            if is_incomplete or is_overlapping:
                line_count = int(result_text.index(tk.END).split(".")[0]) - 2
                tag_name = "incomplete" if is_incomplete else "overlapping"
                result_text.tag_add(tag_name, f"{line_count}.0", f"{line_count}.end")

        #tags for highlighting
        result_text.tag_config("incomplete", background="yellow", foreground="black")
        result_text.tag_config("overlapping", background="orange", foreground="black")

        #create a bar chart of job duration
        fig, ax = plt.subplots(figsize=(5, 3))

        #get durations of completed jobs
        durations = [
            job.get_duration()
            for job in processor.jobs.values()
            if job.is_complete()
        ]
        ax.bar(range(len(durations)), durations)
        ax.set_title("Job Durations")

        #embed the chart in the window
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


#create the main application window
root = tk.Tk()
root.title("Log Analyzer")
tk.Button(root, text="Select Log File", command=analyze_log).pack(pady=5)
result_text = scrolledtext.ScrolledText(root, width=80, height=15)
result_text.pack(padx=10, pady=5)
graph_frame = tk.Frame(root)
graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


root.mainloop()
