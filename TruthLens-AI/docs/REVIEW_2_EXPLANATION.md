# Review 2 Project Status: Product Management System

## Phase-wise Changes for Review 2

This section highlights the specific changes and additions made during the **Review 2** phase, focusing on moving the project from a static frontend interface to a dynamic, database-driven application.

### 1. Problem Statement
The primary problem addressed in Review 2 was the static nature of the initial interface. The system lacked a mechanism to process or store user inputs, meaning any product data entered into the form was lost immediately upon page refresh. We needed a reliable way to make the data entry persistent.

### 2. Objective
The main objective for Review 2 was to implement backend connectivity. Specifically, to build a functional data pipeline that takes the four inputs (Product ID, Product Name, Product Price, and Quantity on Hand) from the HTML form and successfully inserts them into a relational database.

### 3. Requirement Analysis
During this phase, we identified the specific technical requirements needed to bridge the frontend and the database:
- A local server environment (like XAMPP, WAMP, or similar) to execute server-side processing.
- A functional backend script (PHP) capable of capturing `POST` requests.
- A relational database management system (MySQL) to persistently hold the structured product data.

### 4. System Design
The system's architectural design was updated from a standalone static page to a classic Client-Server model:
- **Database Schema**: We designed a new MySQL database table with attributes specifically matching the form fields, assigning correct data types (e.g., Integer for ID/Quantity, Decimal for Price, Varchar for Name).
- **Data Flow Diagram**: We designed the interaction flow: HTML Form -> HTTP POST Request -> PHP Form Handler -> SQL INSERT Query -> MySQL Database.

### 5. Implementation
The core development in this review involved the actual coding of the backend architecture:
- **Database Creation**: Executing DDL commands in MySQL to set up the database and the target table.
- **PHP Integration**: Writing the connection scripts using `mysqli` or `PDO` to securely link the server to the database, and writing logic to extract form `$_POST` variables.
- **Form Binding**: Modifying the existing HTML form, specifically updating the `action` attribute to point to the new PHP script, and ensuring each input `name` attribute exactly matched the backend requirements.

### 6. Testing
Testing for Review 2 strictly focused on the newly implemented data pipelines:
- **Functional Testing**: Inputting various test products to ensure the data successfully travels from the browser to the MySQL table reliably.
- **Connection Testing**: Simulating database downtime or incorrect credentials to ensure the PHP script catches errors gracefully rather than crashing the interface.
- **Data Integrity Testing**: Verifying that number fields don't accept invalid text types being passed back to the database.

### 7. Result
The result of our Review 2 work is a fully functional web-based data entry application. We successfully demonstrated that when a user inputs a product's details and clicks submit, the data is captured, processed, and stored persistently in MySQL, confirming the seamless integration of our technology stack.

### 8. Future Scope
Building upon the foundation of Review 2, the logical next steps for future phases include:
- Implementing Data Retrieval to fetch and display the stored inventory on a dashboard page.
- Adding Edit and Delete capabilities to achieve full CRUD (Create, Read, Update, Delete) functionality.
- Integrating user authentication (Login/Register) to secure the data entry portal.

---

## Role Importance & Summary

To ensure clean code, maintainability, and efficiency, project responsibilities are logically divided by role. Here is a summary of how each discipline contributes to the success of this system.

### Frontend Developer
- **Role Importance**: The frontend dictates the entire user experience. Without an intuitive, clear, and accessible interface, users are prone to making data entry mistakes, regardless of how robust the backend is.
- **Review 2 Summary**: The frontend developer is responsible for structuring the HTML form to capture the exact fields needed (Product ID, Name, Price, Quantity). They also ensure that basic client-side validation is enforced (e.g., making fields required) and perfectly bind the form's HTTP POST configuration to the designated backend script.

### Backend Developer (PHP)
- **Role Importance**: The backend serves as the crucial bridge and gatekeeper. It is responsible for business logic, data sanitization, and guaranteeing that the transition of data from the client to the server is secure and reliable.
- **Review 2 Summary**: The backend developer writes the PHP scripts that receive the HTML form's HTTP requests. They handle the task of safely extracting the input variables, establishing a secure connection to the database, and dynamically generating and executing the SQL `INSERT` commands.

### Database Administrator (MySQL)
- **Role Importance**: The database is the system's single source of truth. Proper architectural setup ensures data integrity, fast retrieval times, and the ability to scale as the business inventory grows from hundreds to thousands of items.
- **Review 2 Summary**: The database administrator is responsible for designing the database schema, selecting the most appropriate and optimized data types (e.g., exact decimals for currency, integers for quantities), and managing the secure credentials that the PHP server uses to connect.
