// Simple validation script to test Contact model schema
// This script validates that the Contact model is properly structured

const Contact = require('../models/Contact.js');

console.log('Contact Model Validation\n');
console.log('='.repeat(50));

// Check if Contact is defined
if (!Contact) {
  console.error('❌ Contact model not found');
  process.exit(1);
}

console.log('✓ Contact model loaded successfully');

// Check schema structure
const schema = Contact.schema;

console.log('\n📋 Schema Fields:');
console.log('- firstName:', schema.path('firstName') ? '✓' : '❌');
console.log('- lastName:', schema.path('lastName') ? '✓' : '❌');
console.log('- email:', schema.path('email') ? '✓' : '❌');
console.log('- phone:', schema.path('phone') ? '✓' : '❌');
console.log('- company:', schema.path('company') ? '✓' : '❌');
console.log('- jobTitle:', schema.path('jobTitle') ? '✓' : '❌');
console.log('- status:', schema.path('status') ? '✓' : '❌');
console.log('- source:', schema.path('source') ? '✓' : '❌');
console.log('- notes:', schema.path('notes') ? '✓' : '❌');
console.log('- tags:', schema.path('tags') ? '✓' : '❌');
console.log('- timestamps:', schema.options.timestamps ? '✓' : '❌');

// Check required fields
console.log('\n🔒 Required Fields:');
const firstNamePath = schema.path('firstName');
const lastNamePath = schema.path('lastName');
const emailPath = schema.path('email');

console.log('- firstName required:', firstNamePath.isRequired ? '✓' : '❌');
console.log('- lastName required:', lastNamePath.isRequired ? '✓' : '❌');
console.log('- email required:', emailPath.isRequired ? '✓' : '❌');
console.log('- email unique:', emailPath.options.unique ? '✓' : '❌');

// Check enums
console.log('\n📝 Enum Values:');
const statusPath = schema.path('status');
const sourcePath = schema.path('source');

console.log('- status enum:', statusPath.enumValues ? statusPath.enumValues.join(', ') : 'not found');
console.log('- status default:', statusPath.defaultValue || 'not set');
console.log('- source enum:', sourcePath.enumValues ? sourcePath.enumValues.join(', ') : 'not found');

// Check indexes
console.log('\n🔍 Indexes:');
const indexes = schema.indexes();
console.log(`- Total indexes: ${indexes.length}`);
indexes.forEach((index, i) => {
  const fields = Object.keys(index[0]).join(', ');
  console.log(`  ${i + 1}. ${fields}`);
});

// Check virtuals
console.log('\n✨ Virtuals:');
const virtuals = schema.virtuals;
console.log('- fullName:', virtuals.fullName ? '✓' : '❌');

console.log('\n' + '='.repeat(50));
console.log('✅ Contact model validation complete!\n');
