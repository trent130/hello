"use server";

export async function loginUser(formData: FormData, csrfToken: string) {
  const email = formData.get("email");
  const password = formData.get("password");

  try {
    const response = await fetch("http://127.0.0.1:8000/user/login/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken, // Include CSRF token in the request header
      },
      body: formData,
      credentials: "include",
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail || "An unexpected error occurred during login"
      );
    }

    const result = await response.json();
    localStorage.setItem("token", result.token); // Store the JWT token
    return { success: true, message: result.message || "Login successful" };
  } catch (error) {
    console.error("Login error:", error);
    throw error;
  }
}