import { memo, useState } from "react";

type ComposerProps = {
  disabled: boolean;
  onSubmit: (text: string) => Promise<void> | void;
};

export const Composer = memo(function Composer({ disabled, onSubmit }: ComposerProps) {
  const [value, setValue] = useState("");

  const submit = async () => {
    const nextValue = value.trim();
    if (!nextValue) {
      return;
    }
    await onSubmit(nextValue);
    setValue("");
  };

  return (
    <form
      className="composer"
      onSubmit={async (event) => {
        event.preventDefault();
        await submit();
      }}
    >
      <textarea
        value={value}
        disabled={disabled}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={async (event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            await submit();
          }
        }}
        rows={3}
        placeholder='Type a request, or use "/skills" / "/prompt"...'
      />
      <div className="composer__actions">
        <button type="submit" disabled={disabled || !value.trim()}>
          Send
        </button>
      </div>
    </form>
  );
});
