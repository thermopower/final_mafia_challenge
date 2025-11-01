/**
 * SearchBar Component
 *
 * 검색어 입력 UI
 */

import React from 'react';
import { Box, TextField, InputAdornment } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  placeholder = '검색어를 입력하세요 (최소 2자)',
}) => {
  return (
    <Box sx={{ width: '100%', maxWidth: 500 }}>
      <TextField
        fullWidth
        size="small"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
};
