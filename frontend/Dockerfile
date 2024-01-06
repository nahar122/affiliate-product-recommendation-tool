# Use an official Node runtime as a parent image
FROM node:21.5.0

# Set the working directory in the container
WORKDIR /usr/src/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY package*.json ./

RUN npm cache clean --force
RUN npm install
RUN npm update


# Define environment variable
ENV PORT 3000

# Start the application using npm start
CMD ["npm", "run", "start"]
