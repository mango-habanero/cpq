import { useState } from 'react';
import { Box, TextField, Typography, Alert } from '@mui/material';
import * as React from 'react';

export interface ContactFormData {
    contact_name: string;
    contact_email: string;
    company?: string;
}

interface ContactFormProps {
    onSubmit: (contactData: ContactFormData) => void;
    loading?: boolean;
    error?: string;
}

interface FormErrors {
    contact_name?: string;
    contact_email?: string;
}

const ContactForm = ({
    onSubmit,
    loading = false,
    error,
}: ContactFormProps) => {
    const [formData, setFormData] = useState<ContactFormData>({
        contact_name: '',
        contact_email: '',
        company: '',
    });

    const [errors, setErrors] = useState<FormErrors>({});

    const validateEmail = (email: string): boolean => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validateForm = (): boolean => {
        const newErrors: FormErrors = {};

        if (!formData.contact_name.trim()) {
            newErrors.contact_name = 'Name is required';
        }

        if (!formData.contact_email.trim()) {
            newErrors.contact_email = 'Email is required';
        } else if (!validateEmail(formData.contact_email)) {
            newErrors.contact_email = 'Please enter a valid email address';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (validateForm()) {
            onSubmit({
                contact_name: formData.contact_name.trim(),
                contact_email: formData.contact_email.trim(),
                company: formData.company?.trim() || undefined,
            });
        }
    };

    const handleFieldChange = (field: keyof ContactFormData, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));

        if (errors[field as keyof FormErrors]) {
            setErrors((prev) => ({ ...prev, [field]: undefined }));
        }
    };

    return (
        <Box
            component="form"
            onSubmit={handleSubmit}
            id="contact-form"
            sx={{ mt: 2 }}
        >
            <Typography variant="h6" sx={{ mb: 3 }}>
                Contact Information
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            <TextField
                fullWidth
                label="Full Name"
                value={formData.contact_name}
                onChange={(e) =>
                    handleFieldChange('contact_name', e.target.value)
                }
                error={!!errors.contact_name}
                helperText={errors.contact_name}
                disabled={loading}
                required
                sx={{ mb: 2 }}
            />

            <TextField
                fullWidth
                label="Email Address"
                type="email"
                value={formData.contact_email}
                onChange={(e) =>
                    handleFieldChange('contact_email', e.target.value)
                }
                error={!!errors.contact_email}
                helperText={errors.contact_email}
                disabled={loading}
                required
                sx={{ mb: 2 }}
            />

            <TextField
                fullWidth
                label="Company (Optional)"
                value={formData.company}
                onChange={(e) => handleFieldChange('company', e.target.value)}
                disabled={loading}
                sx={{ mb: 2 }}
            />

            <button type="submit" style={{ display: 'none' }} />
        </Box>
    );
};

export default ContactForm;
