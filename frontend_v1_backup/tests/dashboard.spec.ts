import { test, expect } from '@playwright/test';

test.describe('Dashboard and Navigation', () => {
  test('Viewer does not see admin links', async ({ page }) => {
    // Mock token setting for a standard viewer
    const tokenPayload = btoa(JSON.stringify({ sub: "user-123", role: "viewer" }));
    const fakeToken = `header.${tokenPayload}.sig`;

    await page.addInitScript((token) => {
      window.localStorage.setItem('token', token);
    }, fakeToken);

    await page.goto('/');

    // Sidebar should be visible
    await expect(page.locator('text="AgentWatch"')).toBeVisible();

    // Verify Dashboard link is visible
    await expect(page.locator('text="Dashboard"')).toBeVisible();

    // Verify Policies link is NOT visible because they are a viewer
    await expect(page.locator('text="Policies"')).not.toBeVisible();
    await expect(page.locator('text="API Keys"')).not.toBeVisible();
  });

  test('Admin sees all links', async ({ page }) => {
    // Mock token setting for an admin
    const tokenPayload = btoa(JSON.stringify({ sub: "user-123", role: "admin" }));
    const fakeToken = `header.${tokenPayload}.sig`;

    await page.addInitScript((token) => {
      window.localStorage.setItem('token', token);
    }, fakeToken);

    await page.goto('/');

    // Sidebar should be visible
    await expect(page.locator('text="AgentWatch"')).toBeVisible();

    // Verify Dashboard link is visible
    await expect(page.locator('text="Dashboard"')).toBeVisible();

    // Verify Policies and API keys are visible
    await expect(page.locator('text="Policies"')).toBeVisible();
    await expect(page.locator('text="API Keys"')).toBeVisible();
  });
});
