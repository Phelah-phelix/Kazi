const express = require('express');
const mysql = require('mysql2');
const bcrypt = require('bcryptjs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Database connection
const db = mysql.createConnection({
    host: 'localhost',
    user: 'phelix', // Replace with your MariaDB username
    password: 'phelix', // Replace with your MariaDB password
    database: 'Kazi' // Replace with your database name
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to MariaDB');
});

// Worker Login
app.post('/api/worker/login', (req, res) => {
    const { email, password } = req.body;
    const query = 'SELECT * FROM users WHERE email = ? AND role = "worker"';
    db.query(query, [email], (err, results) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        if (results.length === 0) return res.status(404).json({ error: 'User not found' });

        const user = results[0];
        const validPassword = bcrypt.compareSync(password, user.password_hash);
        if (!validPassword) return res.status(401).json({ error: 'Invalid password' });

        res.json({ message: 'Login successful', user });
    });
});

// Fetch Worker Profile
app.get('/api/worker/profile', (req, res) => {
    const userId = req.query.userId; // Pass userId from frontend
    const query = 'SELECT * FROM worker_profiles WHERE worker_id = ?';
    db.query(query, [userId], (err, results) => {
        if (err) return res.status(500).json({ error: 'Database error' });
        res.json(results[0]);
    });
});

// Start server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});