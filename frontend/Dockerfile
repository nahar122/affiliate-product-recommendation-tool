# Use an official Node runtime as a parent image
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

# Install any needed packages
RUN npm install --legacy-peer-deps

# Define environment variable
ENV PORT 3000

# Start the application using npm start
CMD ["npm", "start"]
