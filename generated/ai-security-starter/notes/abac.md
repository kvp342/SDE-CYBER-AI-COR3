# ABAC in AWS

## What ABAC is
Attribute-based access control grants access by comparing attributes instead of listing roles. In AWS the attributes are tags on principals and on resources.

## Tag matching
A policy can allow an action only when the resource tag equals the principal tag, using the variable aws:PrincipalTag. One policy then serves every tenant, so adding a tenant needs no new policy.

## Protecting the tags
Users must not be able to change their own tenant tag. Add an explicit deny on tagging actions with the aws:TagKeys condition key.

## RBAC compared
Role-based access control grants permissions per role. It is simple for a few roles but needs a new role or policy for every new tenant.
