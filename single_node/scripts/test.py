import plotext as plt

# Sample data
categories = ['Category A', 'Category B', 'Category C', 'Category D']
values = [10, 24, 15, 30]

# Create a bar graph
plt.bar(categories, values)

# Add labels and title
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Bar Graph')

# Show the plot in the terminal
plt.show()   
