<script>
import axios from "axios";

export default {
  data() {
    return {
      isLogin: true,
      fullName: "",
      username: "",
      email: "",
      phoneNumber: "",
      password: "",
      confirmPassword: "",
      location: "",
      skills: [],
      agreeTerms: false,
    };
  },
  methods: {
    async handleAuth() {
      const endpoint = this.isLogin ? "/api/login/" : "/api/register/";

      // Handle password confirmation for signup
      if (!this.isLogin && this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      // Prepare data to send
      const data = {
        full_name: this.fullName,
        username: this.username,
        email: this.email,
        phone_number: this.phoneNumber,
        password: this.password,
        location: this.location,
        skills: this.skills,
      };

      // Remove confirmPassword for login requests
      if (this.isLogin) {
        delete data.confirmPassword;
      }

      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL || 'http://127.0.0.1:8000'}${endpoint}`, data);

        console.log("Response:", response.data);
        alert(this.isLogin ? "Logged in successfully!" : "Signup successful!");
      } catch (error) {
        console.error("Error:", error.response.data);
        alert("Something went wrong");
      }
    }
  }
};
</script>
