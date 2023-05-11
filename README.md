# mable-cbv

Welcome to Mable, a web-based bug tracker designed to help you manage and prioritize issues and tasks in your software development projects. Whether you're working solo or with a team, Mable provides a streamlined and efficient workflow for reporting, tracking, and resolving issues.
![mable-profile](https://user-images.githubusercontent.com/75034316/225788717-02be66f7-0d8c-4409-aaa0-58df6a82745d.png)
![mable-dashboard](https://user-images.githubusercontent.com/75034316/225788744-32ece86b-0794-472b-b596-e19d429c9f8a.png)
![mable-project-detail](https://user-images.githubusercontent.com/75034316/225788752-644e1816-6ec7-4d17-a94d-a085081eb52c.png)
![mable-ticket-home](https://user-images.githubusercontent.com/75034316/225788757-4a5cf9d6-f07e-473b-b42e-ff7141a7fba3.png)

Mable includes several key features that make it a powerful tool for managing your development projects. These features include:

Multiple user roles: Mable allows you to create and manage different user roles with varying levels of permissions, including admin, developer, and project manager. This ensures that each user can only access the features and data they need to do their job.


Projects and tickets: With Mable, you can create and manage projects, and track progress using tickets. Each ticket can be assigned to a specific user, and is connected to a project. You can also add comments, attachments, and labels to tickets for better organization.

Notifications: Mable provides real-time notifications for updates on tickets you're assigned to, so you can stay on top of issues and tasks without having to constantly check the web app.

Customizable templates: Depending on their user role, each user will have access to different templates to create, read, update, and delete projects and tickets. This allows users to focus on the tasks and information that are most relevant to them.

Overall, Mable is a user-friendly and efficient bug tracker web application that can help you streamline your development projects, prioritize tasks, and manage issues with ease.


To use Mable, you'll need to have the following requirements installed on your local machine:

Python 3.x
Django 3.x
Git
Once you have these installed, follow these steps to set up Mable:

1. Clone the Mable repository from Github using Git:

```git clone https://github.com/your-username/mable.git```

2. Navigate to the project directory:

```cd mable```

3. Create a virtual environment for Mable:

```python3 -m venv env```

4. Activate the virtual environment:

```source env/bin/activate```

5. Install the required dependencies:

```pip install -r requirements.txt```

6. Create the database tables:

```python manage.py migrate```

7. Create a superuser account:

```python manage.py createsuperuser```

8. Start the development server:

```python manage.py runserver```

Once you've completed these steps, you can navigate to http://localhost:8000/ in your web browser to access the Mable web application.

If you want to deploy Mable to a public domain, you can follow these steps:

1. Sign up for a hosting service that supports Django, such as Heroku or PythonAnywhere.

2. Create a new project and connect it to your Mable repository on Github.

3. Set up the necessary environment variables, such as the database credentials and secret key.

4. Deploy your project using the hosting service's deployment tools.

5. Once your project is deployed, you can access it from the public domain provided by the hosting service.
# mable
# mable-cbv
# mable-cbv
