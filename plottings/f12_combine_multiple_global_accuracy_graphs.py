# figure 12

import matplotlib.pyplot as plt
from os import listdir
import sys

log_folders = sys.argv[1:-1]
chosen_device_idx = f"device_{sys.argv[-1]}"

plt.figure(dpi=250)
plt.xlabel('Communication Round')
plt.ylabel('Accuracy')
plt.title('Global model accuracy for {chosen_device_idx}')
plt.legend(loc='center', bbox_to_anchor=(0.32,0.7))

for log_folder in log_folders:
    all_rounds_log_files = []
    list_folders_comm = sorted([f for f in listdir(log_folder) if f.startswith('comm')], key=lambda x: int(x.split('.')[0].split('_')[-1]))
    for f in list_folders_comm:
        for file in listdir(f"{log_folder}/{f}"):
            if file.startswith('accuracy'):
                all_rounds_log_files.append(f"{f}/{file}")
                break

    draw_comm_rounds = len(all_rounds_log_files)

    device_accuracies_across_rounds = []

    for log_file in all_rounds_log_files:
        file = open(f"{log_folder}/{log_file}","r")
        log_whole_text = file.read() 
        lines_list = log_whole_text.split("\n")
        for line in lines_list:
            device_idx = line.split(":")[0].split(" ")[0]
            # if line.startswith('device_1'):
            if device_idx == chosen_device_idx:
                accuracy = round(float(line.split(":")[-1]), 3)
                device_accuracies_across_rounds.append(accuracy)
                break
        file.close()

    device_accuracies_across_rounds = device_accuracies_across_rounds[:draw_comm_rounds]

    # draw graphs over all available comm rounds
    plt.plot(range(draw_comm_rounds), device_accuracies_across_rounds, label=f'Global model accuracy for {chosen_device_idx}')

# plt.savefig(f'plottings_logs/{log_folder.split("/")[1]}_global_model_accuracy_of_{chosen_device_idx}.pdf')
plt.show()

