# Use an official Node.js image for React
FROM node:16

# Set working directory
WORKDIR /frontend

# Copy package.json and install dependencies
COPY package.json /frontend/
RUN npm install

# Copy the rest of the React app
COPY . /frontend/

# Expose port 3000 for React's development server
EXPOSE 3000

# Start the React development server
CMD ["npm", "start"]
