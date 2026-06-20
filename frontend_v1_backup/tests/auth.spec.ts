import { test, expect } from '@playwright/test';

test.describe('Authentication Flows', () => {
  test('User can navigate to the login page', async ({ page }) => {
    // Navigate to the root
    await page.goto('/');

    // Next.js will likely redirect to /login or the layout will show
    // We can also just directly go to /login
    await page.goto('/login');

    // Check that the login page has the Sign In header
    await expect(page.locator('h1')).toContainText('Agentic Watch Login');
    
    // Check that the Email and Password fields exist
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
  });

  test('Invalid login shows error', async ({ page }) => {
    // Mock the backend API call to return a 401
    await page.route('**/auth/login', async route => {
      const json = { detail: "Incorrect email or password" };
      await route.fulfill({ status: 401, json });
    });

    await page.goto('/login');

    // Fill in fake credentials
    await page.locator('input[type="email"]').fill('fake@example.com');
    await page.locator('input[type="password"]').fill('wrongpassword');

    // Submit
    await page.locator('button[type="submit"]').click();

    // Verify error message
    // Assuming the error is shown in the UI
    const errorText = page.locator('text="Incorrect email or password"');
    await expect(errorText).toBeVisible();
  });
});
