# ShopSphere Business Rules

## Core Relationships
- One customer can place many orders.
- One order can contain many order items.
- One product can appear in many order items.
- One product belongs to one category.
- One product belongs to one supplier.
- One order has one payment record.
- One customer can write many reviews.
- One customer can review a product only once.
- Returns are only allowed for valid delivered orders.

## Data Rules
- Stock cannot be negative.
- Email addresses must be unique.
- Order totals must be non-negative.
- Ratings must be between 1 and 5.
- Payment status must be limited to valid values.
