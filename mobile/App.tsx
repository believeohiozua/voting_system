import React, {useState, useEffect} from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import axios from 'axios';

const API_BASE_URL = 'http://10.0.2.2:8000/api'; // Android emulator localhost

interface Feature {
  id: string;
  title: string;
  description: string;
  votes: number;
  created_at: string;
}

function App(): JSX.Element {
  const [features, setFeatures] = useState<Feature[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchFeatures();
  }, []);

  const fetchFeatures = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/features/`);
      setFeatures(response.data);
    } catch (error) {
      console.error('Error fetching features:', error);
      Alert.alert('Error', 'Failed to fetch features');
    }
  };

  const createFeature = async () => {
    if (!title.trim()) {
      Alert.alert('Error', 'Please enter a feature title');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/features/`, {
        title: title.trim(),
        description: description.trim(),
      });
      setTitle('');
      setDescription('');
      fetchFeatures();
      Alert.alert('Success', 'Feature created successfully!');
    } catch (error) {
      console.error('Error creating feature:', error);
      Alert.alert('Error', 'Failed to create feature');
    } finally {
      setLoading(false);
    }
  };

  const upvoteFeature = async (featureId: string) => {
    try {
      await axios.post(`${API_BASE_URL}/features/${featureId}/upvote/`);
      fetchFeatures();
    } catch (error) {
      console.error('Error upvoting feature:', error);
      Alert.alert('Error', 'Failed to upvote feature');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <View style={styles.header}>
          <Text style={styles.title}>Feature Voting System</Text>
        </View>

        <View style={styles.form}>
          <Text style={styles.sectionTitle}>Add New Feature</Text>
          <TextInput
            style={styles.input}
            placeholder="Feature title"
            value={title}
            onChangeText={setTitle}
          />
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="Feature description (optional)"
            value={description}
            onChangeText={setDescription}
            multiline
            numberOfLines={3}
          />
          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={createFeature}
            disabled={loading}>
            <Text style={styles.buttonText}>
              {loading ? 'Creating...' : 'Create Feature'}
            </Text>
          </TouchableOpacity>
        </View>

        <View style={styles.featuresSection}>
          <Text style={styles.sectionTitle}>Features ({features.length})</Text>
          {features.map(feature => (
            <View key={feature.id} style={styles.featureCard}>
              <View style={styles.featureContent}>
                <Text style={styles.featureTitle}>{feature.title}</Text>
                {feature.description ? (
                  <Text style={styles.featureDescription}>
                    {feature.description}
                  </Text>
                ) : null}
              </View>
              <TouchableOpacity
                style={styles.voteButton}
                onPress={() => upvoteFeature(feature.id)}>
                <Text style={styles.voteButtonText}>👍</Text>
                <Text style={styles.voteCount}>{feature.votes}</Text>
              </TouchableOpacity>
            </View>
          ))}
          {features.length === 0 && (
            <Text style={styles.emptyText}>No features yet. Add one above!</Text>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2196F3',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  form: {
    backgroundColor: 'white',
    margin: 16,
    padding: 16,
    borderRadius: 8,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 4,
    padding: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  textArea: {
    height: 80,
    textAlignVertical: 'top',
  },
  button: {
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 4,
    alignItems: 'center',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  featuresSection: {
    margin: 16,
  },
  featureCard: {
    backgroundColor: 'white',
    padding: 16,
    marginBottom: 8,
    borderRadius: 8,
    elevation: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureContent: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
  },
  voteButton: {
    alignItems: 'center',
    padding: 8,
    minWidth: 60,
  },
  voteButtonText: {
    fontSize: 20,
  },
  voteCount: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#2196F3',
    marginTop: 2,
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
    marginTop: 20,
  },
});

export default App;