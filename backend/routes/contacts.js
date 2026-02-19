// contacts.js
// Express router for contact endpoints
// GET /api/contacts - list all contacts (paginated, filterable by status, tags)
// GET /api/contacts/:id - get single contact with full details (including related deals/tickets)
// POST /api/contacts - create new contact (validate required fields)
// PUT /api/contacts/:id - update contact (partial updates allowed)
// DELETE /api/contacts/:id - soft delete (set status to deleted)
// PATCH /api/contacts/:id/notes - add a note to contact

const express = require('express');
const router = express.Router();
const rateLimit = require('express-rate-limit');
const {
  getAllContacts,
  getContactById,
  createContact,
  updateContact,
  deleteContact,
  addNote
} = require('../controllers/contactController');

const contactsLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: { message: 'Too many requests, please try again later.' }
});

router.use(contactsLimiter);

// GET /api/contacts - list all contacts (paginated, filterable by status, tags)
router.get('/', getAllContacts);

// GET /api/contacts/:id - get single contact with full details
router.get('/:id', getContactById);

// POST /api/contacts - create new contact
router.post('/', createContact);

// PUT /api/contacts/:id - update contact (partial updates allowed)
router.put('/:id', updateContact);

// DELETE /api/contacts/:id - soft delete (set status to deleted)
router.delete('/:id', deleteContact);

// PATCH /api/contacts/:id/notes - add a note to contact
router.patch('/:id/notes', addNote);

module.exports = router;
