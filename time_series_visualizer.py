import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=['date'], index_col='date')

# Clean data
lower_quantile = df['value'].quantile(0.025)
upper_quantile = df['value'].quantile(0.975)

#keep only the rows where the value is between the 2.5th and 97.5th percentiles.
df_cleaned = df[(df['value'] >= lower_quantile) & (df['value'] <= upper_quantile)]


def draw_line_plot():
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(14,7))

    # Plot the data
    ax.plot(df_cleaned.index, df_cleaned['value'], color='red', linewidth=1)

    # Set the title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=16)
    ax.set_xlabel("Date", fontsize=14)
    ax.set_ylabel("Page Views", fontsize=14)


    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df_cleaned.copy().reset_index()  # Reset index to get 'date' as a column

    # Extract year and month from date column
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')  # Full month name

    # Define the order of months for the plot
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Convert 'month' column to categorical type
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Group by year and month, then calculate the mean
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 8))
    df_bar.plot(kind='bar', ax=ax)

    ax.set_xlabel("Years", fontsize=14)
    ax.set_ylabel("Average Page Views", fontsize=14)
    ax.legend(title="Months", fontsize=12)

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df_cleaned.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Draw box plots

    # Ensure the 'value' column is of type float
    df_box['value'] = pd.to_numeric(df_box['value'], errors='coerce')

    # Define the order of months for the plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)', fontsize=16)
    axes[0].set_xlabel('Year', fontsize=14)
    axes[0].set_ylabel('Page Views', fontsize=14)

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=month_order)
    axes[1].set_title('Month-wise Box Plot (Seasonality)', fontsize=16)
    axes[1].set_xlabel('Month', fontsize=14)
    axes[1].set_ylabel('Page Views', fontsize=14)
    
    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
