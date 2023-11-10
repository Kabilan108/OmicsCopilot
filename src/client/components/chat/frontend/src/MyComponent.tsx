import React, { useState } from "react"

function MyComponent() {
  const [text, setText] = useState("")
  const [menuVisible, setMenuVisible] = useState(false)

  function handleInputChange(event: React.ChangeEvent<HTMLInputElement>) {
    setText(event.target.value)
    if (event.target.value.includes("@")) {
      setMenuVisible(true)
    } else {
      setMenuVisible(false)
    }
  }

  function handleMenuItemClick(item: string) {
    setText(text + item)
    setMenuVisible(false)
  }

  return (
    <div>
      <input type="text" value={text} onChange={handleInputChange} />
      {menuVisible && (
        <div className="menu">
          {/* Render your menu items here */}
          <div onClick={() => handleMenuItemClick("Item1")}>Item1</div>
          <div onClick={() => handleMenuItemClick("Item2")}>Item2</div>
          // ...
        </div>
      )}
    </div>
  )
}

export default MyComponent
