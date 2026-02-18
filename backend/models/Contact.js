// Contact model for CRM
// Fields:
// - firstName (string, required)
// - lastName (string, required)
// - email (string, unique, required)
// - phone (string)
// - company (string)
// - jobTitle (string)
// - status (enum: lead, customer, churned) default: lead
// - source (enum: website, referral, ad, other)
// - notes (array of { text, date, author })
// - tags (array of strings)
// - createdAt, updatedAt (timestamps)

const mongoose = require('mongoose');

const noteSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true
  },
  date: {
    type: Date,
    default: Date.now
  },
  author: {
    type: String,
    required: true
  }
}, { _id: true });

const contactSchema = new mongoose.Schema({
  firstName: {
    type: String,
    required: [true, 'First name is required'],
    trim: true,
    minlength: [1, 'First name must be at least 1 character'],
    maxlength: [50, 'First name cannot exceed 50 characters']
  },
  lastName: {
    type: String,
    required: [true, 'Last name is required'],
    trim: true,
    minlength: [1, 'Last name must be at least 1 character'],
    maxlength: [50, 'Last name cannot exceed 50 characters']
  },
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    trim: true,
    lowercase: true,
    match: [
      /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
      'Please provide a valid email address'
    ]
  },
  phone: {
    type: String,
    trim: true,
    validate: {
      validator: function(v) {
        // Allow empty string or valid phone format
        return !v || /^[\d\s\-\+\(\)]+$/.test(v);
      },
      message: 'Please provide a valid phone number'
    }
  },
  company: {
    type: String,
    trim: true,
    maxlength: [100, 'Company name cannot exceed 100 characters']
  },
  jobTitle: {
    type: String,
    trim: true,
    maxlength: [100, 'Job title cannot exceed 100 characters']
  },
  status: {
    type: String,
    enum: {
      values: ['lead', 'customer', 'churned'],
      message: 'Status must be one of: lead, customer, churned'
    },
    default: 'lead'
  },
  source: {
    type: String,
    enum: {
      values: ['website', 'referral', 'ad', 'other'],
      message: 'Source must be one of: website, referral, ad, other'
    }
  },
  notes: [noteSchema],
  tags: [{
    type: String,
    trim: true
  }]
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes for performance
contactSchema.index({ email: 1 });
contactSchema.index({ status: 1 });
contactSchema.index({ company: 1 });
contactSchema.index({ createdAt: -1 });
contactSchema.index({ tags: 1 });

// Virtual for full name
contactSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`;
});

// Pre-save middleware to ensure tags are unique
contactSchema.pre('save', function(next) {
  if (this.tags && this.tags.length > 0) {
    this.tags = [...new Set(this.tags)];
  }
  next();
});

const Contact = mongoose.model('Contact', contactSchema);

module.exports = Contact;
