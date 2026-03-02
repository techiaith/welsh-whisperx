#!/usr/bin/env python3
"""
Welsh Verbatim Speech Normalizer - Configurable Version

This module provides configurable normalization for Welsh verbatim speech 
transcriptions. You decide which patterns to normalize.

Usage:
    from welsh_normalizer import WelshNormalizer
    
    # Create with your choices
    normalizer = WelshNormalizer(
        remove_tags=True,
        remove_asterisks=True,
        expand_pronouns=True,
        expand_contractions=True,
        standardize_spelling=True,
        # etc.
    )
    
    result = normalizer.normalize("bo' nw'n gwbod <anadlu> *Facebook*")
"""

import re
import sys
from pathlib import Path

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum

# Handle imports for both module and script execution
try:
    from .tokenization import tokenize_with_punctuation, detokenize
except ImportError:
    # Running as script, add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from tokenization import tokenize_with_punctuation, detokenize

# Import shared Welsh language data
try:
    from .welsh_data import (
        PRONOUN_CORRECTIONS,
        VERB_CONTRACTIONS,
        MAE_CONTRACTIONS,
        OTHER_CONTRACTIONS,
        PLURAL_REDUCTIONS,
        VERB_REDUCTIONS,
        INTERNAL_REDUCTIONS,
        SPELLING_CORRECTIONS,
        HESITATION_STANDARDIZATION,
        MA_FOLLOWERS,
        DI_WEDI_SAFE_PRECEDERS,
        MULTI_WORD_REPLACEMENTS,
    )
except ImportError:
    from normalization.welsh_data import (
        PRONOUN_CORRECTIONS,
        VERB_CONTRACTIONS,
        MAE_CONTRACTIONS,
        OTHER_CONTRACTIONS,
        PLURAL_REDUCTIONS,
        VERB_REDUCTIONS,
        INTERNAL_REDUCTIONS,
        SPELLING_CORRECTIONS,
        HESITATION_STANDARDIZATION,
        MA_FOLLOWERS,
        DI_WEDI_SAFE_PRECEDERS,
        MULTI_WORD_REPLACEMENTS,
    )


class FlagType(Enum):
    """Types of flags for uncertain normalizations."""
    CONTEXT_UNCERTAIN = "context_uncertain"
    REGIONAL_VARIANT = "regional_variant"
    AMBIGUOUS = "ambiguous"


@dataclass
class NormalizationFlag:
    """A flag indicating an uncertain normalization."""
    original: str
    normalized: str
    flag_type: FlagType
    context: str
    position: int
    suggestion: str

    def __str__(self):
        """String representation for CSV serialization."""
        return f"{self.flag_type.value}:{self.original}"


class WelshNormalizer:
    """
    Configurable normalizer for Welsh verbatim speech transcriptions.
    """
    
    def __init__(
        self,
        remove_tags: bool = False,
        remove_asterisks: bool = False,
        expand_pronouns: bool = True,
        expand_verb_contractions: bool = True,
        expand_mae_contractions: bool = True,
        normalize_ma_with_followers: bool = True,  # New: use MA_FOLLOWERS lookup table
        expand_di_contextual: bool = True,  # New: context-aware 'di expansion
        expand_other_contractions: bool = True,
        standardize_plurals: bool = True,
        standardize_verbs: bool = True,
        standardize_internal: bool = True,
        standardize_spelling: bool = True,
        remove_hesitations: bool = False,
        standardize_hesitations: bool = True,
        remove_false_starts: bool = True,
        normalize_whitespace: bool = True,
        flag_uncertain: bool = True,  # New: flag uncertain normalizations
        expand_multi_word: bool = True,  # New: multi-word phrase replacements
        custom_corrections: Optional[Dict[str, str]] = None,
        custom_multi_word: Optional[Dict[str, str]] = None,
    ):
        self.remove_tags = remove_tags
        self.remove_asterisks = remove_asterisks
        self.expand_pronouns = expand_pronouns
        self.expand_verb_contractions = expand_verb_contractions
        self.expand_mae_contractions = expand_mae_contractions
        self.normalize_ma_with_followers = normalize_ma_with_followers
        self.expand_di_contextual = expand_di_contextual
        self.expand_other_contractions = expand_other_contractions
        self.standardize_plurals = standardize_plurals
        self.standardize_verbs = standardize_verbs
        self.standardize_internal = standardize_internal
        self.standardize_spelling = standardize_spelling
        self.remove_hesitations = remove_hesitations
        self.standardize_hesitations = standardize_hesitations
        self.remove_false_starts = remove_false_starts
        self.normalize_whitespace = normalize_whitespace
        self.flag_uncertain = flag_uncertain
        self.expand_multi_word = expand_multi_word

        self._build_corrections(custom_corrections, custom_multi_word)
        
        self._tag_pattern = re.compile(r'<[^>]+>')
        self._asterisk_pattern = re.compile(r'\*([^*]+)\*')
        self._hesitation_pattern = re.compile(r'\b(yy+m*|yrm|ymm*)\b', re.IGNORECASE)
        self._false_start_pattern = re.compile(r'\b\w+-\s')
        self._multi_space_pattern = re.compile(r' +')
    
    def _build_corrections(self, custom: Optional[Dict[str, str]], custom_multi: Optional[Dict[str, str]]):
        self.corrections = {}
        self.multi_word_corrections = {}

        if self.expand_pronouns:
            self.corrections.update(PRONOUN_CORRECTIONS)
        if self.expand_verb_contractions:
            self.corrections.update(VERB_CONTRACTIONS)
        if self.expand_mae_contractions:
            self.corrections.update(MAE_CONTRACTIONS)
        if self.expand_other_contractions:
            self.corrections.update(OTHER_CONTRACTIONS)
        if self.standardize_plurals:
            self.corrections.update(PLURAL_REDUCTIONS)
        if self.standardize_verbs:
            self.corrections.update(VERB_REDUCTIONS)
        if self.standardize_internal:
            self.corrections.update(INTERNAL_REDUCTIONS)
        if self.standardize_spelling:
            self.corrections.update(SPELLING_CORRECTIONS)
        if self.standardize_hesitations:
            self.corrections.update(HESITATION_STANDARDIZATION)
        if custom:
            self.corrections.update(custom)

        if self.expand_multi_word:
            self.multi_word_corrections.update(MULTI_WORD_REPLACEMENTS)
        if custom_multi:
            self.multi_word_corrections.update(custom_multi)

        self.corrections_lower = {k.lower(): v.lower() for k, v in self.corrections.items()}

        # Build lookup structure for multi-word patterns
        # Group by number of words for efficient matching
        self.multi_word_by_length = {}
        for phrase, replacement in self.multi_word_corrections.items():
            phrase_lower = phrase.lower()
            word_count = len(phrase_lower.split())
            if word_count not in self.multi_word_by_length:
                self.multi_word_by_length[word_count] = {}
            self.multi_word_by_length[word_count][phrase_lower] = replacement
    
    

    def normalize(self, text: str) -> str:
        """
        Apply normalization and return the result.

        Returns:
            Normalized text
        """
        result, _ = self.normalize_with_flags(text)
        return result

    def normalize_with_flags(self, text: str) -> Tuple[str, List[NormalizationFlag]]:
        """
        Apply normalization and return both result and any flags.

        Returns:
            Tuple of (normalized_text, list_of_flags)
        """
        if not text:
            return text, []

        flags = []
        result = text

        if self.remove_tags:
            result = self._tag_pattern.sub('', result)

        if self.remove_asterisks:
            result = self._asterisk_pattern.sub(r'\1', result)

        if self.remove_hesitations:
            result = self._hesitation_pattern.sub('', result)

        if self.remove_false_starts:
            result = self._false_start_pattern.sub('', result)

        if self.corrections or self.multi_word_corrections or self.normalize_ma_with_followers or self.expand_di_contextual:
            result, new_flags = self._apply_corrections(result, text)
            flags.extend(new_flags)

        if self.normalize_whitespace:
            result = self._multi_space_pattern.sub(' ', result)
            result = result.strip()

        return result, flags
    
    def _apply_corrections(self, text: str, full_text: str) -> Tuple[str, List[NormalizationFlag]]:
        # Tokenize with punctuation separation
        tokens =  tokenize_with_punctuation(text)

        # Extract just the words for processing
        word_indices = [i for i, (token, ttype) in enumerate(tokens) if ttype == 'word']

        flags = []
        i = 0  # Index in word_indices

        while i < len(word_indices):
            token_idx = word_indices[i]
            word = tokens[token_idx][0]
            word_lower = word.lower()

            # Get context (previous and next words, not punctuation)
            prev_word = tokens[word_indices[i-1]][0].lower() if i > 0 else None
            next_word = tokens[word_indices[i+1]][0].lower() if i + 1 < len(word_indices) else None

            # Try multi-word patterns first (check longest patterns first)
            multi_word_match = False
            if self.expand_multi_word:
                for word_count in sorted(self.multi_word_by_length.keys(), reverse=True):
                    if i + word_count <= len(word_indices):
                        # Build the potential phrase from current position
                        phrase_word_indices = [word_indices[i+j] for j in range(word_count)]
                        phrase_words = [tokens[idx][0] for idx in phrase_word_indices]
                        phrase_lower = ' '.join(w.lower() for w in phrase_words)

                        if phrase_lower in self.multi_word_by_length[word_count]:
                            # Found a match!
                            replacement = self.multi_word_by_length[word_count][phrase_lower]

                            # Preserve capitalization of first word
                            if phrase_words[0][0].isupper():
                                replacement = replacement[0].upper() + replacement[1:]

                            # Replace all matched word tokens with the replacement
                            tokens[phrase_word_indices[0]] = (replacement, 'word')
                            # Remove the other matched word tokens
                            for idx in reversed(phrase_word_indices[1:]):
                                # Find and remove spaces between words too
                                if idx > 0 and tokens[idx-1][1] == 'space':
                                    tokens.pop(idx-1)
                                    # Adjust indices after removal
                                    word_indices = [wi - 1 if wi > idx-1 else wi for wi in word_indices]
                                    idx -= 1
                                tokens.pop(idx)
                                # Adjust word_indices after removal
                                word_indices = [wi - 1 if wi > idx else wi for wi in word_indices]

                            i += word_count  # Skip all words in the matched phrase
                            multi_word_match = True
                            break

                    if multi_word_match:
                        break

            if multi_word_match:
                continue

            # Handle ma' with MA_FOLLOWERS lookup table
            if word_lower == "ma'" and self.normalize_ma_with_followers:
                # ma' becomes mae
                ma_normalized = "Mae" if word[0].isupper() else "mae"
                tokens[token_idx] = (ma_normalized, 'word')

                # Check if next word should be normalized
                if next_word and next_word in MA_FOLLOWERS:
                    normalized_follower = MA_FOLLOWERS[next_word]
                    next_token_idx = word_indices[i + 1]
                    tokens[next_token_idx] = (normalized_follower, 'word')
                    i += 2  # Skip both ma' and the follower
                    continue
                else:
                    i += 1
                    continue

            # Handle 'di with context
            elif word_lower == "'di" and self.expand_di_contextual:
                if prev_word and prev_word.rstrip("'") in DI_WEDI_SAFE_PRECEDERS:
                    tokens[token_idx] = ("wedi", 'word')
                else:
                    # Keep as-is
                    if self.flag_uncertain:
                        flag = NormalizationFlag(
                            original=word,
                            normalized=word,
                            flag_type=FlagType.CONTEXT_UNCERTAIN,
                            context=f"...'di not preceded by pronoun",
                            position=i,
                            suggestion="'di not preceded by pronoun - keeping as-is"
                        )
                        flags.append(flag)
                i += 1
                continue

            # Regular word corrections
            if word in self.corrections:
                tokens[token_idx] = (self.corrections[word], 'word')
            elif word_lower in self.corrections_lower:
                replacement = self.corrections_lower[word_lower]
                if word[0].isupper():
                    replacement = replacement.capitalize()
                tokens[token_idx] = (replacement, 'word')
            # else: keep token as-is

            i += 1

        return detokenize(tokens), flags

    def get_flags_summary(self, flags: List[NormalizationFlag]) -> str:
        """Generate a human-readable summary of flags."""
        if not flags:
            return "No uncertain cases flagged."

        lines = [f"Found {len(flags)} uncertain case(s):", ""]
        for i, flag in enumerate(flags, 1):
            lines.append(f"{i}. '{flag.original}' at position {flag.position}")
            lines.append(f"   Context: {flag.context}")
            lines.append(f"   Suggestion: {flag.suggestion}")
            lines.append("")

        return "\n".join(lines)

    def describe_config(self) -> str:
        lines = ["Welsh Normalizer Configuration:", "=" * 40]
        settings = [
            ("Remove non-speech tags", self.remove_tags),
            ("Remove asterisks", self.remove_asterisks),
            ("Expand pronouns (nw->nhw)", self.expand_pronouns),
            ("Expand verb contractions (ca'l->cael)", self.expand_verb_contractions),
            ("Expand mae contractions (ma'->mae)", self.expand_mae_contractions),
            ("Normalize ma' with followers (ma' nw->mae nhw)", self.normalize_ma_with_followers),
            ("Expand 'di contextually (dwi 'di->dwi wedi)", self.expand_di_contextual),
            ("Standardize plurals (petha->pethau)", self.standardize_plurals),
            ("Standardize verbs (dechre->dechrau)", self.standardize_verbs),
            ("Standardize internal (gwbod->gwybod)", self.standardize_internal),
            ("Standardize spelling", self.standardize_spelling),
            ("Remove hesitations", self.remove_hesitations),
            ("Flag uncertain cases", self.flag_uncertain),
        ]
        for name, enabled in settings:
            status = "ON" if enabled else "OFF"
            lines.append(f"  [{status}] {name}")
        return "\n".join(lines)

    def normalize_srt_file(self, srt_path: str, output_path: Optional[str] = None, include_original: bool = False) -> str:
        """
        Normalize the subtitle text content of an SRT file.

        Args:
            srt_path: Path to the input SRT file
            output_path: Optional path for the output file. If None, returns normalized content.
            include_original: If True, include original text above normalized text

        Returns:
            The normalized SRT content as a string
        """
        # Read the SRT file
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse SRT format: sequence number, timestamp, subtitle text, blank line
        normalized_lines = []
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Check if this is a sequence number (digits only)
            if line.isdigit():
                normalized_lines.append(line)
                i += 1

                # Next line should be timestamp
                if i < len(lines):
                    timestamp_line = lines[i].strip()
                    normalized_lines.append(timestamp_line)
                    i += 1

                    # Collect subtitle text until blank line
                    subtitle_lines = []
                    while i < len(lines) and lines[i].strip():
                        subtitle_lines.append(lines[i])
                        i += 1

                    # Normalize the subtitle text
                    subtitle_text = '\n'.join(subtitle_lines)
                    normalized_text = self.normalize(subtitle_text)

                    # Add original and normalized text
                    if include_original:
                        normalized_lines.append(subtitle_text)
                        normalized_lines.append(normalized_text)
                    else:
                        normalized_lines.append(normalized_text)

                    # Add blank line separator
                    normalized_lines.append('')
            else:
                # Skip empty lines or malformed content
                i += 1

        # Join all lines
        result = '\n'.join(normalized_lines)

        # Write to output file if specified
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)

        return result


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Welsh text normalizer - normalize text or SRT subtitle files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Normalize example text
  python welsh_normalizer.py --text "bo' nw'n gwbod"

  # Normalize an SRT file
  python welsh_normalizer.py --srt input.srt

  # Normalize an SRT file and save to output file
  python welsh_normalizer.py --srt input.srt --output output.srt

  # Normalize with original text included above normalized text
  python welsh_normalizer.py --srt input.srt --output output.srt --include-original
        '''
    )

    # Create mutually exclusive group for input type
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--text',
        type=str,
        help='Text to normalize'
    )
    input_group.add_argument(
        '--srt',
        type=str,
        help='Path to SRT file to normalize'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (only for SRT files)'
    )

    parser.add_argument(
        '--include-original',
        action='store_true',
        help='Include original text above normalized text in SRT output'
    )

    parser.add_argument(
        '--show-config',
        action='store_true',
        help='Show normalizer configuration'
    )

    args = parser.parse_args()

    # Create normalizer instance
    normalizer = WelshNormalizer()

    # Show configuration if requested
    if args.show_config:
        print(normalizer.describe_config())
        print()

    # Process text input
    if args.text:
        if args.output:
            print("Warning: --output is ignored for text input")

        normalized = normalizer.normalize(args.text)
        print("Original:")
        print(args.text)
        print("\nNormalized:")
        print(normalized)

    # Process SRT file input
    elif args.srt:
        if args.include_original and not args.srt:
            print("Warning: --include-original only applies to SRT files")

        try:
            normalized = normalizer.normalize_srt_file(
                args.srt,
                args.output,
                include_original=args.include_original
            )

            if args.output:
                print(f"Normalized SRT file saved to: {args.output}")
            else:
                print("Normalized SRT content:")
                print(normalized)

        except FileNotFoundError:
            print(f"Error: File not found: {args.srt}")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing SRT file: {e}")
            sys.exit(1)