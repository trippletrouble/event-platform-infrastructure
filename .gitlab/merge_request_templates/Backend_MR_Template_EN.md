# General MR
### Describe your changes
>
## User Story ID and link
- User Story ID:
- Issue Link:
### Checklist before requesting a review
- [ ] I have pulled and merged the master branch into my feature branch
- [ ] I have performed a self-review of my code
- [ ] The code is properly formatted
- [ ] The feature is fully finished and ready for review
- [ ] This MR is targeting the developer branch
- [ ] I have removed all debug code and console logs
- [ ] I have created a wiki entry about this feature
- [ ] If it is a core feature, I have added thorough tests (if applicable)
- [ ] The added tests are passing (if applicable)
---
# Backend Specific

## Functionality & API Design
- [ ] All affected endpoints conform to the OpenAPI specification (`docs/swagger.yml`)
- [ ] For new or modified endpoints, the OpenAPI specification has been updated
- [ ] RESTful principles are followed (correct HTTP methods, status codes, resource naming)
- [ ] Hypermedia links are included in responses where appropriate (HATEOAS)
- [ ] Input validation is implemented for all endpoints (DTOs with class-validator or similar)
- [ ] Error responses follow a consistent format (`ErrorResponseDto`)

## Authentication & Authorization
- [ ] Protected endpoints verify authentication (OAuth / Session)
- [ ] Role-based access control is correctly implemented (Admin vs. Company)
- [ ] Unauthorized access attempts are properly rejected with `401`/`403`

## Database
- [ ] Prisma schema changes are checked in via migration (`prisma migrate`)
- [ ] New relations have explicit `onDelete` rules
- [ ] FK columns have `@@index` directives for query performance
- [ ] Seed data is updated if the schema has changed
- [ ] All database changes are documented in the wiki

## Tests
- [ ] Unit tests for service logic are in place and passing
- [ ] Integration tests for new/modified endpoints are in place and passing
- [ ] Edge cases and error scenarios are covered (invalid inputs, missing permissions, resources not found)
- [ ] All existing tests are still passing

## Documentation
- [ ] Wiki entry for the feature has been created or updated
- [ ] Complex logic is commented in the code (why, not what)