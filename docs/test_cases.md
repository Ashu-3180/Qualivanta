# Planned test case inventory

All statuses below are **planned, not executed**. `Automation candidate` identifies the approximately 27 cases intended for initial automation after APK inspection. Other cases are planned for manual execution, diagnostic checks, or further evaluation. The actual app must be inspected before any case is implemented.

## Authentication — 10 cases

| ID | Scenario | Type | Expected outcome | Automation status |
|---|---|---|---|---|
| AUTH-01 | Login screen and required controls are visible. | Functional | Required controls are displayed. | Planned automation candidate |
| AUTH-02 | Valid demo credentials open the catalog. | Smoke | Catalog opens. | Planned automation candidate |
| AUTH-03 | Invalid username produces appropriate feedback. | Negative | Clear validation or authentication feedback appears. | Planned automation candidate |
| AUTH-04 | Invalid password produces appropriate feedback. | Negative | Clear validation or authentication feedback appears. | Planned automation candidate |
| AUTH-05 | Empty username is handled correctly. | Negative | Submission is prevented or appropriate feedback appears. | Planned automation candidate |
| AUTH-06 | Empty password is handled correctly. | Negative | Submission is prevented or appropriate feedback appears. | Planned automation candidate |
| AUTH-07 | Empty username and password are handled correctly. | Negative | Submission is prevented or appropriate feedback appears. | Planned automation candidate |
| AUTH-08 | Malformed email is rejected, if applicable. | Negative | Invalid format is rejected when the app validates email format. | Further evaluation |
| AUTH-09 | Password characters are masked. | Functional | Password input is obscured. | Planned automation candidate |
| AUTH-10 | Valid login works after a failed attempt. | Regression | A later valid attempt opens the catalog. | Further evaluation |

## Catalog and product details — 12 cases

| ID | Scenario | Type | Expected outcome | Automation status |
|---|---|---|---|---|
| CAT-01 | Catalog is displayed after successful login. | Smoke | Catalog screen and expected content appear. | Planned automation candidate |
| CAT-02 | Product list contains product cards. | Functional | Product cards are present. | Planned automation candidate |
| CAT-03 | Product names are displayed correctly. | Functional | Names match verified app data. | Manual execution |
| CAT-04 | Product prices are displayed correctly. | Functional | Prices match verified app data. | Manual execution |
| CAT-05 | Product images are visible. | Functional | Product images render. | Manual execution |
| CAT-06 | Selecting a product opens its details. | Functional | The product detail screen opens. | Planned automation candidate |
| CAT-07 | Detail-page name matches the selected product. | Functional | Detail name matches the selected catalog item. | Planned automation candidate |
| CAT-08 | Detail-page price matches the catalog. | Functional | Detail price matches the catalog price. | Planned automation candidate |
| CAT-09 | Back navigation returns to the catalog. | Functional | Back returns to the prior catalog state. | Manual execution |
| CAT-10 | Name-based sorting works in ascending order. | Functional | Products are ordered ascending by name. | Planned automation candidate |
| CAT-11 | Price sorting works in ascending order. | Functional | Products are ordered ascending by price. | Planned automation candidate |
| CAT-12 | Scrolling exposes additional products. | Functional | Additional products become accessible. | Manual execution |

## Shopping cart — 10 cases

| ID | Scenario | Type | Expected outcome | Automation status |
|---|---|---|---|---|
| CART-01 | Adding a product updates the cart badge. | Smoke | Badge reflects the added item. | Planned automation candidate |
| CART-02 | The added product appears in the cart. | Functional | Cart contains the selected product. | Planned automation candidate |
| CART-03 | Adding another product retains both items. | Functional | Both products remain in the cart. | Planned automation candidate |
| CART-04 | Cart items and quantities are correct. | Functional | Items and quantities match actions. | Manual execution |
| CART-05 | A product can be removed from the cart. | Functional | Selected product is removed. | Planned automation candidate |
| CART-06 | Removing all products displays the empty state. | Functional | Empty-cart state is displayed. | Planned automation candidate |
| CART-07 | Continue Shopping returns to the catalog. | Functional | Catalog is displayed. | Manual execution |
| CART-08 | Subtotal matches the displayed line-item values. | Functional | Subtotal equals the verified line-item calculation. | Planned automation candidate |
| CART-09 | Cart state persists through navigation where expected. | Regression | Cart state is retained where supported. | Further evaluation |
| CART-10 | Repeated additions behave consistently. | Regression | Repeated actions follow verified app behavior. | Further evaluation |

## Checkout — 10 cases

| ID | Scenario | Type | Expected outcome | Automation status |
|---|---|---|---|---|
| CHK-01 | A populated cart proceeds to checkout. | Smoke | Checkout opens from a populated cart. | Planned automation candidate |
| CHK-02 | Required checkout fields are displayed. | Functional | Required fields are visible. | Manual execution |
| CHK-03 | Submitting an empty form is handled correctly. | Negative | Submission is prevented or validation appears. | Planned automation candidate |
| CHK-04 | Missing first name is handled correctly. | Negative | First-name validation appears. | Manual execution |
| CHK-05 | Missing last name is handled correctly. | Negative | Last-name validation appears. | Manual execution |
| CHK-06 | Missing postal code is handled correctly. | Negative | Postal-code validation appears. | Manual execution |
| CHK-07 | Valid information proceeds to the summary. | Functional | Valid data opens the summary. | Planned automation candidate |
| CHK-08 | Summary includes selected items and quantities. | Functional | Summary reflects selected items and quantities. | Manual execution |
| CHK-09 | Final total matches the expected calculation. | Functional | Total matches the verified calculation. | Planned automation candidate |
| CHK-10 | Completing checkout displays confirmation. | Smoke | Completion confirmation appears. | Planned automation candidate |

## Navigation and framework reliability — 8 cases

| ID | Scenario | Type | Expected outcome | Automation status |
|---|---|---|---|---|
| SYS-01 | Navigation menu opens and displays available options. | Functional | Menu and supported options appear. | Manual execution |
| SYS-02 | Logout returns to the login screen, if supported. | Functional | Login screen appears when logout is supported. | Further evaluation |
| SYS-03 | Android Back navigation behaves correctly. | Functional | Back follows the verified navigation contract. | Manual execution |
| SYS-04 | A cold app launch reaches the expected initial screen. | Smoke | Expected initial screen appears after a cold launch. | Planned automation candidate |
| SYS-05 | Test setup isolates state between test executions. | Regression | Each test starts from controlled state. | Diagnostic check |
| SYS-06 | Failure screenshots are attached to the HTML report. | Regression | Failed test evidence is attached. | Diagnostic check |
| SYS-07 | Logcat diagnostics are saved for failing tests. | Regression | Relevant Logcat output is saved. | Diagnostic check |
| SYS-08 | HTML report contains execution results and summary. | Regression | Report contains results and summary. | Diagnostic check |

## Candidate summary

The initial candidate set is AUTH-01 through AUTH-07 and AUTH-09; CAT-01, CAT-02, CAT-06, CAT-07, CAT-08, CAT-10, and CAT-11; CART-01, CART-02, CART-03, CART-05, CART-06, and CART-08; CHK-01, CHK-03, CHK-07, CHK-09, and CHK-10; and SYS-04: 27 cases total. Candidate labels are planning targets, not evidence of implementation or execution.
