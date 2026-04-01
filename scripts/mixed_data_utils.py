"""
🔄 MIXED DATASET & DYNAMIC INJECTION UTILITIES
Generates realistic mixed normal/malicious data for testing
"""

import pandas as pd
import numpy as np
from typing import Tuple, List

def inject_malicious_to_row(normal_row, attack_intensity=1.0):
    """
    Inject malicious patterns into a single normal EEG row dynamically
    CRITICAL: Must use real column names from the dataset
    
    Args:
        normal_row: Normal EEG feature row (pandas Series or numpy array)
        attack_intensity: Strength of attack (1.0 = standard, 2.0 = 2x stronger)
    
    Returns:
        Malicious row with same shape as input
    """
    row = np.array(normal_row, dtype=float)
    
    # 🔥 STRONG ATTACK PATTERN - Amplify all features
    row = row * np.random.uniform(6.0 * attack_intensity, 12.0 * attack_intensity)
    
    # Add heavy random noise to create detectable anomalies
    noise = np.random.normal(0, 5.0 * attack_intensity, row.shape)
    row = row + noise
    
    # Ensure some values are extremely high/low (characteristic of malicious EEG)
    row[np.random.randint(0, len(row))] *= np.random.uniform(3.0, 8.0)
    
    return row


def create_mixed_test_data(
    normal_samples: int = 10,
    malicious_samples: int = 10,
    random_seed: int = None,
    attack_intensity: float = 1.0
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Create realistic mixed dataset with randomly interspersed malicious packets
    Perfect for real-world scenario testing
    
    Args:
        normal_samples: Number of normal packets
        malicious_samples: Number of malicious packets to inject
        random_seed: For reproducibility (None = random each time)
        attack_intensity: Strength of malicious injection
    
    Returns:
        Tuple of (mixed_dataframe, is_malicious_array)
        - mixed_dataframe: DataFrame with mixed data
        - is_malicious_array: Boolean array indicating which are malicious
    
    Example:
        df_mixed, is_mal = create_mixed_test_data(normal_samples=7, malicious_samples=3)
        # Results in 10 packets with ~3 randomly marked as malicious
    """
    
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Load base normal data
    df_full = pd.read_csv("data/processed/eeg_features.csv")
    
    # Sample normal rows
    normal_indices = np.random.choice(len(df_full), size=normal_samples, replace=False)
    normal_data = df_full.iloc[normal_indices].reset_index(drop=True)
    
    # Randomly select which positions to inject malicious data
    total_packets = normal_samples + malicious_samples
    malicious_positions = np.random.choice(
        total_packets, 
        size=malicious_samples, 
        replace=False
    )
    
    # Mark which are malicious
    is_malicious = np.zeros(total_packets, dtype=bool)
    is_malicious[malicious_positions] = True
    
    # Create mixed dataset
    mixed_rows = []
    malicious_idx = 0
    
    for i in range(total_packets):
        if is_malicious[i]:
            # Inject malicious patterns
            normal_row = df_full.iloc[np.random.randint(0, len(df_full))]
            malicious_row = inject_malicious_to_row(normal_row, attack_intensity)
            mixed_rows.append(malicious_row)
        else:
            # Use normal data
            normal_row = normal_data.iloc[malicious_idx if malicious_idx < len(normal_data) else 0]
            mixed_rows.append(normal_row.values)
            malicious_idx += 1
    
    df_mixed = pd.DataFrame(mixed_rows, columns=df_full.columns)
    
    return df_mixed, is_malicious


def create_realistic_stream_test(
    total_packets: int = 20,
    injection_rate: float = 0.3,
    random_seed: int = None
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Create a realistic packet stream with random malicious injection rate
    
    Args:
        total_packets: Total packets to generate
        injection_rate: Percentage of packets to inject (0.0-1.0)
            - 0.3 = 30% malicious, 70% normal
        random_seed: For reproducibility
    
    Returns:
        Tuple of (stream_dataframe, is_malicious_array)
    """
    
    malicious_count = max(1, int(total_packets * injection_rate))
    normal_count = total_packets - malicious_count
    
    return create_mixed_test_data(
        normal_samples=normal_count,
        malicious_samples=malicious_count,
        random_seed=random_seed,
        attack_intensity=1.0
    )


def print_test_summary(df_mixed: pd.DataFrame, is_malicious: np.ndarray):
    """
    Print a summary of the mixed test data
    """
    print("\n" + "=" * 60)
    print("📊 MIXED TEST DATASET SUMMARY")
    print("=" * 60)
    print(f"Total packets:      {len(df_mixed)}")
    print(f"Normal packets:      {np.sum(~is_malicious)}")
    print(f"Malicious packets:   {np.sum(is_malicious)}")
    print(f"Injection rate:      {(np.sum(is_malicious)/len(df_mixed))*100:.1f}%")
    print(f"Data shape:          {df_mixed.shape}")
    print("\nPacket distribution:")
    
    for i, is_mal in enumerate(is_malicious):
        status = "🔴 MALICIOUS" if is_mal else "🟢 NORMAL"
        print(f"  Packet {i+1:2d}: {status}")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    
    # Example 1: Create mixed data
    print("EXAMPLE 1: Create realistic mixed test")
    df_mixed, is_mal = create_mixed_test_data(normal_samples=7, malicious_samples=3)
    print_test_summary(df_mixed, is_mal)
    
    # Example 2: Create realistic stream
    print("\nEXAMPLE 2: Create realistic stream with 30% injection")
    df_stream, is_mal_stream = create_realistic_stream_test(
        total_packets=10,
        injection_rate=0.3,
        random_seed=42  # reproducible
    )
    print_test_summary(df_stream, is_mal_stream)
