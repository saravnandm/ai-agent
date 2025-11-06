import AsyncStorage from "@react-native-async-storage/async-storage";
import uuid from "react-native-uuid";

const getUserId = async () => {
  let id = await AsyncStorage.getItem("user_id");
  if (!id) {
    id = uuid.v4();
    await AsyncStorage.setItem("user_id", id);
  }
  return id;
};
export { getUserId };