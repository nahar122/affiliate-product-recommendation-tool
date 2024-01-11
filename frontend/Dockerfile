# Use a", "run", "start"
# Use an official Node runtime as a parent image
FROM node:21.5.0

RUN npm install -g react-scripts
# Set the working directory in the container
WORKDIR /usr/src/frontend

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./
RUN npm install
COPY . .
# Define environment variable
EXPOSE 5173

# Start the application using npm start
CMD ["npm", "run", "dev", "--host"]

