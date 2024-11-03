# To-Do List for "nestdict" Project

## Project: NestDict - Simplifying Nested Dictionary Operations

### Objectives

The "nestdict" project aims to create a Python library that simplifies working with nested dictionaries. It will address common issues developers face when dealing with nested dictionaries and provide features to enhance dictionary manipulation, key access, serialization, and more.

### Project Plan

#### Phase 1: Implement Core Features

Core features includes - easily performing operations like accessing/updating/deleting nested keys

#### Phase 2: Implement Schema Validation and setting fields immutable

* Json/dict data will be validated against the schema provided
* Data will be dynamically validated, means each update/delete operation will be executed after validation.
* Immutable fields will be defined in the schema and won't be updated/deleted once initialized.