// contactController.js
// getAllContacts: implement pagination, filtering, sorting
// getContactById: populate deals and tickets if needed
// createContact: validate input, check for duplicate email, save
// updateContact: find and update, return updated doc
// deleteContact: soft delete by setting status='deleted'
// addNote: push a note object to notes array

const Contact = require('../models/Contact');

/**
 * getAllContacts
 * GET /api/contacts
 * Supports pagination (page, limit), filtering by status and tags, and sorting.
 */
const getAllContacts = async (req, res) => {
  try {
    const {
      page = 1,
      limit = 20,
      status,
      tags,
      sort = '-createdAt'
    } = req.query;

    const filter = { status: { $ne: 'deleted' } };

    if (status && status !== 'deleted') {
      filter.status = status;
    }

    if (tags) {
      const tagList = Array.isArray(tags) ? tags : tags.split(',').map(t => t.trim());
      filter.tags = { $in: tagList };
    }

    const pageNum = Math.max(1, parseInt(page, 10));
    const limitNum = Math.min(100, Math.max(1, parseInt(limit, 10)));
    const skip = (pageNum - 1) * limitNum;

    const [contacts, total] = await Promise.all([
      Contact.find(filter).sort(sort).skip(skip).limit(limitNum),
      Contact.countDocuments(filter)
    ]);

    res.json({
      data: contacts,
      pagination: {
        total,
        page: pageNum,
        limit: limitNum,
        totalPages: Math.ceil(total / limitNum)
      }
    });
  } catch (err) {
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

/**
 * getContactById
 * GET /api/contacts/:id
 * Returns a single contact. Placeholder populate for deals and tickets when those models exist.
 */
const getContactById = async (req, res) => {
  try {
    const contact = await Contact.findById(req.params.id);

    if (!contact || contact.status === 'deleted') {
      return res.status(404).json({ message: 'Contact not found' });
    }

    res.json({ data: contact });
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ message: 'Invalid contact ID' });
    }
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

/**
 * createContact
 * POST /api/contacts
 * Validates required fields, checks for duplicate email, then saves the new contact.
 */
const createContact = async (req, res) => {
  try {
    const { firstName, lastName, email, phone, company, jobTitle, status, source, tags } = req.body;

    if (!firstName || !lastName || !email) {
      return res.status(400).json({ message: 'firstName, lastName, and email are required' });
    }

    const existing = await Contact.findOne({ email: email.trim().toLowerCase() });
    if (existing) {
      return res.status(409).json({ message: 'A contact with this email already exists' });
    }

    const contact = new Contact({ firstName, lastName, email, phone, company, jobTitle, status, source, tags });
    await contact.save();

    res.status(201).json({ data: contact });
  } catch (err) {
    if (err.name === 'ValidationError') {
      return res.status(400).json({ message: 'Validation error', errors: err.errors });
    }
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

/**
 * updateContact
 * PUT /api/contacts/:id
 * Finds the contact and applies partial updates, then returns the updated document.
 */
const updateContact = async (req, res) => {
  try {
    // Prevent clients from bypassing soft delete or setting status to 'deleted' via this endpoint
    const existing = await Contact.findById(req.params.id);
    if (!existing || existing.status === 'deleted') {
      return res.status(404).json({ message: 'Contact not found' });
    }

    const update = { ...req.body };
    if (update.status === 'deleted') {
      return res.status(400).json({ message: 'Use DELETE endpoint to remove a contact' });
    }

    const contact = await Contact.findByIdAndUpdate(
      req.params.id,
      { $set: update },
      { new: true, runValidators: true }
    );

    res.json({ data: contact });
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ message: 'Invalid contact ID' });
    }
    if (err.name === 'ValidationError') {
      return res.status(400).json({ message: 'Validation error', errors: err.errors });
    }
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

/**
 * deleteContact
 * DELETE /api/contacts/:id
 * Soft deletes a contact by setting its status to 'deleted'.
 */
const deleteContact = async (req, res) => {
  try {
    const contact = await Contact.findByIdAndUpdate(
      req.params.id,
      { $set: { status: 'deleted' } },
      { new: true }
    );

    if (!contact) {
      return res.status(404).json({ message: 'Contact not found' });
    }

    res.json({ message: 'Contact deleted successfully', data: contact });
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ message: 'Invalid contact ID' });
    }
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

/**
 * addNote
 * PATCH /api/contacts/:id/notes
 * Pushes a new note object (text, author) to the contact's notes array.
 */
const addNote = async (req, res) => {
  try {
    const { text, author } = req.body;

    if (!text || !author) {
      return res.status(400).json({ message: 'text and author are required for a note' });
    }

    const existing = await Contact.findById(req.params.id);
    if (!existing || existing.status === 'deleted') {
      return res.status(404).json({ message: 'Contact not found' });
    }

    const contact = await Contact.findByIdAndUpdate(
      req.params.id,
      { $push: { notes: { text, author, date: new Date() } } },
      { new: true, runValidators: true }
    );

    res.json({ data: contact });
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ message: 'Invalid contact ID' });
    }
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

module.exports = {
  getAllContacts,
  getContactById,
  createContact,
  updateContact,
  deleteContact,
  addNote
};
