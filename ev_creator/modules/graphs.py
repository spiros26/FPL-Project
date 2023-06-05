import matplotlib.pyplot as plt
import seaborn as sns

def count_barplot(data_counts, label_name):
    # Set the style to 'fivethirtyeight'
    plt.style.use('fivethirtyeight')

    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    # Customize color palette
    colors = sns.color_palette('pastel')[:len(data_counts)]

    # Create the bar plot with custom colors
    bars = plt.bar(data_counts.index, data_counts.values, color=colors)

    plt.xlabel(label_name)  
    plt.ylabel('Count')
    plt.title('Bar Plot of ' + label_name) 

    # Add labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, height,
                ha='center', va='bottom', fontweight='bold', fontsize=9)

    # Remove top and right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # Customize tick parameters
    plt.tick_params(axis='x', which='both', bottom=False)
    plt.tick_params(axis='y', which='both', left=False)

    # Adjust y-axis limit for better visualization
    plt.ylim(top=max(data_counts.values) * 1.1)

    # Add gridlines
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Add a horizontal line at the mean value
    mean_value = data_counts.mean()
    plt.axhline(y=mean_value, color='gray', linestyle='--', linewidth=1.5)
    plt.text(len(data_counts) - 0.9, mean_value, f'Mean: {mean_value:.2f}', color='gray',
            ha='right', va='bottom', fontweight='bold', fontsize=9)

    plt.tight_layout()  # Improve spacing between elements
    plt.show()



def scatterplot(df, x_col, y_col, color_col):
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed

    zero_npg_mask = df[color_col] == 0
    
    plt.scatter(df[x_col][zero_npg_mask], df[y_col][zero_npg_mask], color='red', label= color_col+ ' = 0', alpha=0.5)
    
    plt.scatter(df[x_col][~zero_npg_mask], df[y_col][~zero_npg_mask], c=df[color_col][~zero_npg_mask], cmap='viridis', label=color_col+ ' != 0', alpha=0.5)
    
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'Scatter Plot of {x_col} vs {y_col}')
    plt.legend()
    
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()



def plot_percentages(df, column_name, start_value, end_value, window_size, col):
    num_windows = int((end_value - start_value) / window_size)

    if num_windows == 6:
        num_rows = 2
        num_cols = 3
    else:
        num_rows = 1
        num_cols = num_windows

    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 8))
    fig.subplots_adjust(wspace=0.4, hspace=0.6)

    # Define custom colors for the pie chart slices
    colors = ['#1f77b4', '#ff7f0e']

    for i, ax in enumerate(axs.flat):
        if i < num_windows:
            window_start = start_value + i * window_size
            window_end = window_start + window_size

            # Filter the DataFrame based on the specified window of values
            windowed_df = df[(df[column_name] >= window_start) & (df[column_name] <= window_end)]

            # Calculate the number of samples within the specified window
            num_samples = len(windowed_df)
            windowed_npg_not_zero = windowed_df[windowed_df[col] != 0]
            window_percentage = (len(windowed_npg_not_zero) / num_samples) * 100

            windowed_npg_zero = windowed_df[windowed_df[col] == 0]
            zero_percentage = (len(windowed_npg_zero) / num_samples) * 100

            # Create a pie chart
            labels = [col+' != 0', col+' = 0']
            percentages = [window_percentage, zero_percentage]
            explode = (0.1, 0)  # Explode the 'npg != 0' slice

            # Customize the pie chart aesthetics
            wedgeprops = {'width': 0.4, 'edgecolor': 'white'}  # Set the width and edge color of the pie slices
            textprops = {'fontsize': 12}  # Set the fontsize of the pie chart labels

            ax.pie(percentages, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
                   wedgeprops=wedgeprops, textprops=textprops, pctdistance=0.85)
            ax.axis('equal')  # Ensure an equal aspect ratio for a circular pie chart
            ax.set_title(f"{column_name}\n({window_start} to {window_end})\n(Samples: {num_samples})", fontsize=12, wrap=True)
        else:
            ax.axis('off')  # Disable empty subplots

    plt.tight_layout()
    plt.show()

